import { TQuestion } from '../../../../../../shared/components/survey/types';

export const qHaveOwnersInsurance: TQuestion = {
  id: 'qHaveOwnersInsurance',
  type: 'radio',
  title: 'Do you have Homeowner’s insurance?',
  options: [
    {
      optionId: 'ownerInsuranceYes',
      label: 'Yes',
      // tags: ['Housing - Owner with Insurance']
      tags: ['housing-owner-with-insurance'],
    },
    {
      optionId: 'housingInsuranceNo',
      label: 'No',
      // tags: ['Housing - No Insurance']
      tags: ['housing-no-insurance'],
    },
  ],
  rules: {
    required: true,
  },
};
