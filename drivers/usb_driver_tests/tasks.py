import cffi
...
""" Build the CFFI Python bindings """
print_banner("Building CFFI Module")
ffi = cffi.FFI()

this_dir = pathlib.Path.absolute()