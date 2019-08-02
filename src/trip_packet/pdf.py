#!/usr/bin/env python

import collections

import PyPDF2


class PdfReader():

    def _BT(self, operands):
        self.page_state['local']['text_matrix'] = None
        self.page_state['local']['text_shows'] = []

    def _ET(self, operands):
        for text_show in self.page_state['local']['text_shows']:
            self.page_state['global']['lines'][
                self.page_state['local']['text_matrix'][5]].append((
                    self.page_state['local']['text_matrix'][4], text_show))

        self.page_state['local']['text_matrix'] = None
        self.page_state['local']['text_shows'] = []

    def _Tm(self, operands):
        self.page_state['local']['text_matrix'] = operands

    def _TJ(self, operands):
        self.page_state['local']['text_shows'].append(operands[0])

    def _clear_page_state(self):
        self.page_state = {
            'local': {
                'text_matrix': None,
                'text_shows': []},
            'global': {
                'lines': collections.defaultdict(list)}}

    def _render_lines(self):
        line_numbers = sorted(
            self.page_state['global']['lines'].keys(), reverse = True)

        page = []
        for line_number in line_numbers:
            text_shows = sorted(
                self.page_state['global']['lines'][line_number],
                key=lambda x: x[0])

            line = ''
            for text_show in text_shows:
                for operand in text_show[1]:
                    if isinstance(operand, PyPDF2.generic.TextStringObject):
                        line += operand
            page.append(line)
    
        return page

    def __init__(self, filename):
        self.handle = open(filename, 'rb')
        self.pypdf2_reader = PyPDF2.PdfFileReader(self.handle)

        self._clear_page_state()

    def num_pages(self):
        return self.pypdf2_reader.numPages

    def get_page(self, page_num):
        pypdf2_page = self.pypdf2_reader.getPage(page_num)

        pypdf2_content = pypdf2_page["/Contents"].getObject()
        if not isinstance(pypdf2_content, PyPDF2.pdf.ContentStream):
            pypdf2_content = PyPDF2.pdf.ContentStream(
                pypdf2_content, pypdf2_page.pdf)
    
        self._clear_page_state()
        for operands, operator in pypdf2_content.operations:
            if operator == b'BT':
                self._BT(operands)
            elif operator == b'ET':
                self._ET(operands)
            elif operator == b'Tm':
                self._Tm(operands)
            elif operator == b'TJ':
                self._TJ(operands)

        return self._render_lines()

