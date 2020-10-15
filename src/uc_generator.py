import argparse
import json

from md_adapter import MarkdownAdapter
from tex_adapter import LatexAdapter

PROGRAM_DESC = 'use case document generator'

JSON_FP_ARG = 'json_fp'
JSON_FP_HELP = 'json file path'

EXPORT_FORMAT_ARG = 'export_format'
EXPORT_FORMAT_HELP = 'export format (markdown, latex)'
MARKDOWN_EXPORT_FORMAT = 'md'
LATEX_EXPORT_FORMAT = 'tex'

EXPORT_PATH_ARG_SHORT = '-o'
EXPORT_PATH_ARG_LONG = '--output'
EXPORT_PATH_HELP = 'export file path'
EXPORT_PATH_DEST = 'export_fp'

JSON_EXT = '.json'
MARKDOWN_EXT = '.md'
LATEX_EXT = '.tex'

md = MarkdownAdapter()
tex = LatexAdapter()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=PROGRAM_DESC)
    parser.add_argument(
            JSON_FP_ARG, 
            help=JSON_FP_HELP)
    parser.add_argument(
            EXPORT_FORMAT_ARG,
            choices = [MARKDOWN_EXPORT_FORMAT, LATEX_EXPORT_FORMAT],
            help=EXPORT_FORMAT_HELP)
    parser.add_argument(
            EXPORT_PATH_ARG_SHORT,
            EXPORT_PATH_ARG_LONG,
            help=EXPORT_PATH_HELP,
            dest=EXPORT_PATH_DEST)
    args = parser.parse_args()

    with open(args.json_fp, 'r') as json_f:
        adapter = None
        file_ext = ''
        if args.export_format == MARKDOWN_EXPORT_FORMAT:
            file_ext = MARKDOWN_EXT
            adapter = md
        elif args.export_format == LATEX_EXPORT_FORMAT:
            file_ext = LATEX_EXT
            adapter = tex
        json_data = json.load(json_f)
        adapter.convert_data(json_data)
        
        file_name = args.json_fp.split('/')[-1]
        if file_name[-len(JSON_EXT): len(file_name)] == JSON_EXT:
            file_name = file_name[:-len(JSON_EXT)]

        if args.export_fp:
            if args.export_fp[-1] == '/':
                file_name = args.export_fp + file_name + file_ext
            else:
                file_name = args.export_fp
                if file_name[-len(file_ext): len(file_name)] != file_ext:
                    file_name += file_ext
        else: 
            file_name += file_ext
        adapter.export(file_name)
