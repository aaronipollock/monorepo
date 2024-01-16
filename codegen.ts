import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  overwrite: true,
  schema: 'apps/betterangels-backend/schema.graphql',
  documents: 'libs/expo/betterangels/src/lib/apollo/graphql/**/*.ts',
  generates: {
    'libs/expo/betterangels/src/lib/apollo/gql-types/': {
      preset: 'client',
      plugins: [],
    },
  },
};

export default config;