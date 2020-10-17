from uc_adapter import UseCaseAdapter

class MarkdownAdapter(UseCaseAdapter):
    
    def __init__(self):
        UseCaseAdapter.__init__(self)

        self.TITLE = '## __{id}: {uc}__\n'
        self.SECTION = '\n__{s}:__ '
        self.EXTENSION_SECTION = '\n* __Extension {i}:__ {e}\n'
        self.UNORDERED_ITEM = '- {item}\n'
        self.ORDERED_ITEM = '{i}. {item}\n'
        self.EXTENSION_ITEM = '\n\t{i}.{j} {item}\n'

        self.USE_CASE = self.SECTION.format(s='Use case')
        self.PRIMARY_ACTOR = self.SECTION.format(s='Primary actor')
        self.SCOPE = self.SECTION.format(s='Scope')
        self.LEVEL = self.SECTION.format(s='Level')
        self.STAKEHOLDERS = self.SECTION.format(s='Stakeholders')
        self.PRECONDITIONS = self.SECTION.format(s='Preconditions')
        self.POSTCONDITIONS = self.SECTION.format(s='Postconditions')
        self.NOMINAL_CASE = self.SECTION.format(s='Nominal case')
        self.EXTENSIONS = self.SECTION.format(s='Extensions')
        self.OTHER = self.SECTION.format(s='Other')

    def _reset_text_data(self):
        self.text_data['title'] = ''
        self.text_data['use_case'] = self.USE_CASE
        self.text_data['primary_actor'] = self.PRIMARY_ACTOR
        self.text_data['scope'] = self.SCOPE
        self.text_data['level'] = self.LEVEL
        self.text_data['stakeholders'] = self.STAKEHOLDERS
        self.text_data['preconditions'] = self.PRECONDITIONS
        self.text_data['postconditions'] = self.POSTCONDITIONS
        self.text_data['nominal_case'] = self.NOMINAL_CASE
        self.text_data['extensions'] = self.EXTENSIONS
        self.text_data['other'] = self.OTHER

    def _convert_unordered_list(self, item_str, items):
        unordered_list = '\n\n'
        for item in items:
            item_text = item_str.format(item=item)
            unordered_list += item_text
        return unordered_list

    def _convert_ordered_list(self, item_str, items):
        ordered_list = '\n\n'
        for i in range(len(items)):
            item_text = item_str.format(i=i+1, item=items[i])
            ordered_list += item_text

        return ordered_list

    def _convert_extension_steps(self, step_str, nominal_step, steps):
        extension_steps = ''
        for i in range(len(steps)):
            step_text = step_str.format(i=nominal_step, j=i, item=steps[i])
            extension_steps += step_text 

        return extension_steps 

    def convert_data(self, json_data):
        UseCaseAdapter.convert_data(self, json_data)
        self._reset_text_data()

        self.text_data['title'] = self.TITLE.format(
                id=self.data['id'],
                uc=self.data['use_case'])
        self.text_data['use_case'] += self.data['use_case'] + '\n'
        self.text_data['primary_actor'] += self.data['primary_actor'] + '\n'
        self.text_data['scope'] += self.data['scope'] + '\n'
        self.text_data['level'] += self.data['level'] + '\n'
        self.text_data['other'] += self.data['other'] + '\n'

        stakeholders_text = ''
        if len(self.data['stakeholders']) > 1:
            goals = [stakeholder['goal'] \
                    for stakeholder \
                    in self.data['stakeholders']]
            stakeholders_text = self._convert_unordered_list(
                    self.UNORDERED_ITEM, 
                    goals)
        elif len(self.data['stakeholders']) > 0:
            stakeholders_text = self.data['stakeholders'][0]['goal'] + '\n'
        self.text_data['stakeholders'] += stakeholders_text         

        preconditions_text = self._convert_ordered_list(
                self.ORDERED_ITEM,
                self.data['preconditions'])
        self.text_data['preconditions'] += preconditions_text

        postconditions_text = self._convert_ordered_list(
                self.ORDERED_ITEM,
                self.data['postconditions'])
        self.text_data['postconditions'] += postconditions_text

        nominal_case_text = self._convert_ordered_list(
                self.ORDERED_ITEM,
                self.data['nominal_case'])
        self.text_data['nominal_case'] += nominal_case_text

        extensions_text = '\n'
        for extension in self.data['extensions']:
            extension_str = self.EXTENSION_SECTION.format(
                i=extension['nominal_step'],
                e=extension['extension'])
            steps_text = self._convert_extension_steps(
                    self.EXTENSION_ITEM,
                    extension['nominal_step'],
                    extension['steps'])
            extensions_text += extension_str + steps_text
        self.text_data['extensions'] += extensions_text
