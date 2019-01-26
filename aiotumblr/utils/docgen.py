# encoding=utf-8
import sys
import logging
import os.path
from importlib import import_module

from setuptools import Command
from distutils.errors import DistutilsOptionError

from aiotumblr.extensions.base import Extension

__all__ = ['DocGenTypeException', 'DocGenCommand']

log = logging.getLogger(__name__)
_library_root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

try:
    from jinja2 import Template
except ImportError:  # Jinja2 is included with sphinx, is available as dev-package when doing documentation
    log.error('DocGen requires Jinja2 to be installed')
    raise sys.exit(1)


class DocGenTypeException(TypeError):
    pass


class DocGenCommand(Command):
    description = 'Generate documentation from the extension files'

    user_options = [
        ('include-base', None, 'Generate docs for core library as well. This includes the PublicAPI'),
        ('generate-index', None, 'Re-generate index.rst as well based on all the extensions seen'),
        ('extension=', None, 'Extension(s) to generate documentation for; format as `filename:ClassName` e.g. '
                             '`public:PublicAPI`, comma separated'),
        ('output-dir=', 'o', 'Output directory for the generated RST files; defaults to the sources on the '
                             'docs folder outside of this library')
    ]

    boolean_options = [
        'include-base',
        'generate-index'
    ]

    # noinspection PyAttributeOutsideInit
    def initialize_options(self):
        self.include_base = None
        self.extension = None
        self.output_dir = None
        self.generate_index = None

    # noinspection PyAttributeOutsideInit
    def finalize_options(self):
        if not self.include_base and self.extension is None:
            raise DistutilsOptionError('Either `--include_base` or `--extension` has to be set (or both).')
        if self.extension:
            if ',' in self.extension:
                # noinspection PyUnresolvedReferences
                _exts = self.extension.split(',')
            else:
                _exts = [self.extension]

            self.extension = []
            for ext in _exts:
                _ext = ext.split(':')
                if len(_ext) != 2:
                    raise DistutilsOptionError('`--extension` has to be formatted as `filename:ClassName`.')
                self.extension.append(_ext)
        if self.output_dir:
            if not os.path.isdir(self.output_dir):
                raise DistutilsOptionError('`--output-dir` has to be an existing directory.')
        else:
            self.output_dir = os.path.join(os.path.dirname(_library_root_path), 'docs', 'source')

    def run(self):
        toc_tree_contents = []

        # TODO: Treat this as a regular extension, and use `include_base` purely for the base or, make it static?
        if self.include_base:
            from aiotumblr_ext.extensions.public import PublicAPIExtension
            docs = PublicAPIExtension.generate_docs()
            if not self.dry_run:
                with open(os.path.join(self.output_dir, f'{PublicAPIExtension.prefix}.rst'), 'w') as fp:
                    self.announce(f'Writing documentation for {PublicAPIExtension.prefix!r}...')
                    fp.write(docs)
                    toc_tree_contents.append(PublicAPIExtension.prefix)
            else:
                self.announce(f'Skipping writing documentation for {PublicAPIExtension.prefix!r} (dry run)...')

        if self.extension:
            for ext_path, class_name in self.extension:
                mod = import_module(f'aiotumblr_ext.extensions.{ext_path}')
                api = getattr(mod, class_name)

                if not issubclass(api, Extension):
                    self.warn(str(api))
                    raise DocGenTypeException('Extension passed with `--extension` should be a subclass of '
                                              '`aiotumblr.extensions.base.Exception`. Got passed an instance of type '
                                              f'{type(api)!r} instead.')

                docs = api.generate_docs()
                if not self.dry_run:
                    with open(os.path.join(self.output_dir, f'{api.prefix}.rst'), 'w') as fp:
                        self.announce(f'Writing documentation for {api.prefix!r}...')
                        fp.write(docs)
                        toc_tree_contents.append(api.prefix)
                else:
                    self.announce(f'Skipping writing documentation for {api.prefix!r} (dry run)...')

        if self.generate_index:
            _indices = []
            for f in toc_tree_contents:
                _indices.append(f'   {f}\n')

            if not self.dry_run:
                with open(os.path.join(self.output_dir, 'index.rst'), 'w') as fp:
                    self.announce('Writing index...')
                    fp.writelines([
                        'Welcome to AIOTumblr\'s documentation!\n',
                        '=====================================\n',
                        '\n',
                        '.. toctree::\n',
                        '   :maxdepth: 2\n',
                        '   :caption: Contents:\n',
                        '\n',
                        'extensions',
                        '\n',
                        *_indices,
                        '\n',
                        '\n',
                        'Indices and tables\n',
                        '==================\n',
                        '\n',
                        '* :ref:`genindex`\n',
                        '* :ref:`search`\n',
                        '\n',
                    ])
            else:
                self.announce('Skipping writing index (dry run)...')
