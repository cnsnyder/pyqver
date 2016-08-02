import pyqver2

class PyqverCommand(setuptools.Command):
    """The :class:`Pyqver` class is used by setuptools to perform
    checks on registered modules.
    """

    description = "Run pyqver on modules registered in setuptools"
    user_options = []

    def initialize_options(self):
        self.option_to_cmds = {}
        parser = get_parser()[0]
        for opt in parser.option_list:
            cmd_name = opt._long_opts[0][2:]
            option_name = cmd_name.replace('-', '_')
            self.option_to_cmds[option_name] = opt
            setattr(self, option_name, None)

    def finalize_options(self):
        self.options_dict = {}
        for (option_name, opt) in self.option_to_cmds.items():
            if option_name in ['help', 'verbose']:
                continue
            value = getattr(self, option_name)
            if value is None:
                continue
            value = option_normalizer(value, opt, option_name)
            # Check if there's any values that need to be fixed.
            if option_name == "include" and isinstance(value, str):
                value = re.findall('[^,;\s]+', value)

            self.options_dict[option_name] = value

    def distribution_files(self):
        if self.distribution.packages:
            package_dirs = self.distribution.package_dir or {}
            for package in self.distribution.packages:
                pkg_dir = package
                if package in package_dirs:
                    pkg_dir = package_dirs[package]
                elif '' in package_dirs:
                    pkg_dir = package_dirs[''] + os.path.sep + pkg_dir
                yield pkg_dir.replace('.', os.path.sep)

        if self.distribution.py_modules:
            for filename in self.distribution.py_modules:
                yield "%s.py" % filename
        # Don't miss the setup.py file itself
        yield "setup.py"

    def run(self):
        # Prepare
        paths = list(self.distribution_files())
        flake8_style = get_style_guide(paths=paths, **self.options_dict)

        # Run the checkers
        report = flake8_style.check_files()
        exit_code = print_report(report, flake8_style)
        if exit_code > 0:
            raise SystemExit(exit_code > 0)
