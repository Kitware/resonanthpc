import glob
import os
import shutil
import xml.etree.ElementInclude as EI
import xml.etree.ElementTree as ET

def resolve_xinclude(source_folder, source_ext, output_folder):
    """"""
    # Process all files in the source folder with the give extension
    pattern = '{}/*{}'.format(source_folder, source_ext)
    matches= glob.glob(pattern)
    for filepath in matches:
        tree = ET.parse(filepath)
        root = tree.getroot()
        EI.include(root)  # resolves xi:include elements

        # Write output file
        filename = os.path.basename(filepath)
        basename, ext = os.path.splitext(filename)
        out_filename = '{}.sbt'.format(basename)
        out_filepath = os.path.join(output_folder, out_filename)
        with open(out_filepath, 'wb') as f:
            s = ET.tostring(root)
            # TODO: would be good to clean up trailing whitespace
            #       however, we'd have to do some str-bytes conversion
            # s = "\n".join([ln.strip() for ln in s.splitlines()])
            f.write(s)
            print('Wrote', out_filepath)
    return


# def copy_files_with_extension(source_folder, source_ext, output_folder):
#     files = glob.glob(os.path.join(source_folder, "*"+source_ext))
#     for fn in files:
#         target = os.path.join(output_folder, os.path.basename(fn))
#         shutil.copyfile(fn, target)
#     return


if __name__ == '__main__':
    # Used hard-coded paths
    start_folder = os.path.abspath(os.path.dirname(__file__))
    source_folder = os.path.join(start_folder, 'source')
    # build_folder = os.path.join(start_folder, "build")
    # if os.path.exists(build_folder):
    #     shutil.rmtree(build_folder)
    # os.mkdir(build_folder)

    # Resolve the xincludes and create `sbt` files
    source_ext = '.sbs'
    resolve_xinclude(source_folder, source_ext, start_folder)
    # Copy over all remaining `sbt` files
    # source_ext = '.sbt'
    # copy_files_with_extension(source_folder, source_ext, build_folder)
