import { gql } from '@apollo/client';

// NOTE: we need to pass in an email from some recovery process
export const GENERATE_MAGIC_LINK_MUTATION = gql`
  mutation GenerateMagicLink {
    generateMagicLink(data: { email: "paul+test@betterangels.la" }) {
      message
    }
  }
`;

export const CREATE_NOTE = gql`
  mutation CreateNote($data: CreateNoteInput!) {
    createNote(data: $data) {
      id
      title
      body
      createdAt
      createdBy {
        id
        username
        email
      }
    }
  }
`;

export const UPDATE_NOTE = gql`
  mutation UpdateNote($data: UpdateNoteInput!) {
    updateNote(data: $data) {
      id
      title
      body
      createdAt
      createdBy {
        id
        username
        email
      }
    }
  }
`;