class UseCaseAdapter:
    
    def __init__(self):
        self.data = {
                'id': '',
                'use_case': '',
                'primary_actor': '',
                'scope': '',
                'level': '',
                'stakeholders': [],
                'preconditions': [],
                'postconditions': [],
                'nominal_case': [],
                'extensions': [],
                'other': ''
                }

        self.text_data = {
                'title': '',
                'use_case': '',
                'primary_actor': '',
                'scope': '',
                'level': '',
                'stakeholders': '',
                'preconditions': '',
                'postconditions': '',
                'nominal_case': '',
                'extensions': '',
                'other': ''
                }

    def validate_data(self, json_data):
        pass

    def convert_data(self, json_data): 
        self.data['id'] = json_data['id']
        self.data['use_case'] = json_data['useCase']
        self.data['primary_actor'] = json_data['primaryActor']
        self.data['scope'] = json_data['scope']
        self.data['level'] = json_data['level']
        self.data['other'] = json_data['other']

        for s in json_data['stakeholders']:
            stakeholder = {}
            stakeholder['stakeholder'] = s['stakeholder']
            stakeholder['goal'] = s['goal']
            self.data['stakeholders'].append(stakeholder)

        for precondition in json_data['preconditions']:
            self.data['preconditions'].append(precondition)

        for postcondition in json_data['postconditions']:
            self.data['postconditions'].append(postcondition)

        for step in json_data['nominalCase']:
            self.data['nominal_case'].append(step)

        for e in json_data['extensions']:
            extension = {}
            extension['extension'] = e['extension']
            extension['nominal_step'] = e['nominalStep']
            extension['steps'] = []
            for e_step in e['steps']:
                extension['steps'].append(e_step)
            self.data['extensions'].append(extension)

    def export(self, fp):
        with open(fp, 'w') as f:
            f_text = self.text_data['title'] \
                    + self.text_data['use_case'] \
                    + self.text_data['primary_actor'] \
                    + self.text_data['scope'] \
                    + self.text_data['level'] \
                    + self.text_data['stakeholders'] \
                    + self.text_data['preconditions'] \
                    + self.text_data['postconditions'] \
                    + self.text_data['nominal_case'] \
                    + self.text_data['extensions'] \
                    + self.text_data['other']

            f.write(f_text)
            f.close()
