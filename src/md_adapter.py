from uc_adapter import UseCaseAdapter

class MarkdownAdapter(UseCaseAdapter):
    
    def __init__(self):
        UseCaseAdapter.__init__(self)

        self.TITLE = '## __{id}: {title}__\n'
        self.SECTION = '\n__{section}:__ '
        self.EXTENSION_SECTION = '* __Extension {i}:__ {extension}\n'
        self.UNORDERED_ITEM = '- {item}\n'
        self.ORDERED_ITEM = '{i}. {item}\n'
        self.EXTENSION_ITEM = '\n\t{i}.{j} {item}\n'

        self.USE_CASE = self.SECTION.format(section='Use case')
        self.PRIMARY_ACTOR = self.SECTION.format(section='Primary actor')
        self.SCOPE = self.SECTION.format(section='Scope')
        self.LEVEL = self.SECTION.format(section='Level')
        self.STAKEHOLDERS = self.SECTION.format(section='Stakeholders')
        self.PRECONDITIONS = self.SECTION.format(section='Preconditions')
        self.POSTCONDITIONS = self.SECTION.format(section='Postconditions')
        self.NOMINAL_CASE = self.SECTION.format(section='Nominal case')
        self.EXTENSIONS = self.SECTION.format(section='Extensions')
        self.OTHER = self.SECTION.format(section='Other')
        
        self.EXTENSION_DATA = {
                'subsection': '',
                'steps': []
                }

        self.data = {
                'title': '',
                'use_case': '',
                'primary_actor': '',
                'scope': '',
                'stakeholders': {
                    'section': '',
                    'items': [] 
                    },
                'preconditions': {
                    'section': '',
                    'items': []
                    },
                'postconditions': {
                    'section': '',
                    'items': []
                    },
                'nominal_case': {
                    'section': '',
                    'items': []
                    },
                'extensions': {
                    'section': '',
                    'items': []
                    },
                'other': ''
                }

    def convert_data(self, data):
        self.data['title'] = self.TITLE.format(
                id=data['id'],
                title=data['title'])
        self.data['use_case'] = self.USE_CASE + data['title'] + '\n'
        self.data['primary_actor'] = self.PRIMARY_ACTOR + data['primaryActor'] \
                + '\n'
        self.data['scope'] = self.SCOPE + data['scope'] + '\n' 
        self.data['level'] = self.LEVEL + data['level'] + '\n'
        
        self.data['stakeholders']['section'] = self.STAKEHOLDERS
        stakeholder_str = '{item}\n'
        if len(data['stakeholders']) > 1:
            self.data['stakeholders']['section'] += '\n\n'
            stakeholder_str = self.UNORDERED_ITEM

        for s in data['stakeholders']:
            item = stakeholder_str.format(item=s['goal']) 
            self.data['stakeholders']['items'].append(item)

        self.data['preconditions']['section'] = self.PRECONDITIONS + '\n\n'
        for i in range(len(data['preconditions'])):
            item = self.ORDERED_ITEM.format(
                    i=i+1, 
                    item=data['preconditions'][i])
            self.data['preconditions']['items'].append(item)

        self.data['postconditions']['section'] = self.POSTCONDITIONS + '\n\n'
        for i in range(len(data['postconditions'])):
            item = self.ORDERED_ITEM.format(
                    i=i+1,
                    item=data['postconditions'][i])
            self.data['postconditions']['items'].append(item)

        self.data['nominal_case']['section'] = self.NOMINAL_CASE + '\n\n'
        for i in range(len(data['nominalCase'])):
            item = self.ORDERED_ITEM.format(
                    i=i+1,
                    item=data['nominalCase'][i])
            self.data['nominal_case']['items'].append(item)

        self.data['extensions']['section'] = self.EXTENSIONS + '\n\n'
        extensions = data['extensions']
        for e in extensions:
            item = { 'subsection': '', 'steps': [] }
            item['subsection'] = self.EXTENSION_SECTION.format(
                    i=e['nominalStep'], 
                    extension=e['name']) 
            for j in range(len(e['steps'])):
                step = self.EXTENSION_ITEM.format(
                        i=e['nominalStep'], 
                        j=j+1,
                        item=e['steps'][j])
                item['steps'].append(step)
            item['steps'][-1] += '\n'
            self.data['extensions']['items'].append(item)

        self.data['other'] = self.OTHER + data['other']

    def export(self, fp):
        with open(fp, 'w') as f:
            f.write(self.data['title'])
            f.write(self.data['use_case'])
            f.write(self.data['primary_actor'])
            f.write(self.data['scope'])
            f.write(self.data['level'])
            
            f.write(self.data['stakeholders']['section'])
            for s in self.data['stakeholders']['items']:
                f.write(s)

            f.write(self.data['preconditions']['section'])
            for p in self.data['preconditions']['items']:
                f.write(p)

            f.write(self.data['postconditions']['section'])
            for p in self.data['postconditions']['items']:
                f.write(p)

            f.write(self.data['nominal_case']['section'])
            for nc in self.data['nominal_case']['items']:
                f.write(nc)

            f.write(self.data['extensions']['section'])
            for e in self.data['extensions']['items']:
                f.write(e['subsection'])
                for s in e['steps']:
                    f.write(s)

            f.write(self.data['other'])
            f.close()
