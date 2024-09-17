from typing import Any, Dict

from clients.enums import (
    ClientDocumentNamespaceEnum,
    EyeColorEnum,
    GenderEnum,
    HairColorEnum,
    HmisAgencyEnum,
    LanguageEnum,
    LivingSituationEnum,
    MaritalStatusEnum,
    PronounEnum,
    RaceEnum,
    RelationshipTypeEnum,
    YesNoPreferNotToSayEnum,
)
from common.tests.utils import GraphQLBaseTestCase
from dateutil.relativedelta import relativedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


class ClientProfileGraphQLBaseTestCase(GraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.EXPECTED_CLIENT_AGE = 20
        self.date_of_birth = timezone.now().date() - relativedelta(years=self.EXPECTED_CLIENT_AGE)
        self.client_profile_fields = """
            id
            address
            age
            dateOfBirth
            displayCaseManager
            displayPronouns
            eyeColor
            gender
            hairColor
            heightInInches
            hmisId
            livingSituation
            maritalStatus
            nickname
            phoneNumber
            physicalDescription
            placeOfBirth
            preferredLanguage
            profilePhoto {
                name
            }
            pronouns
            pronounsOther
            race
            spokenLanguages
            veteranStatus
            contacts {
                id
                name
                email
                phoneNumber
                mailingAddress
                relationshipToClient
                relationshipToClientOther
            }
            hmisProfiles {
                id
                hmisId
                agency
            }
            householdMembers {
                id
                name
                dateOfBirth
                gender
                relationshipToClient
                relationshipToClientOther
            }
            user {
                id
                firstName
                lastName
                middleName
                email
            }
        """

        # Force login the case manager to create client fixtures
        self.graphql_client.force_login(self.org_1_case_manager_1)
        self._setup_clients()
        self._setup_client_documents()
        # Logout after setting up client fixtures
        self.graphql_client.logout()

    def _setup_clients(self) -> None:
        self.client_profile_1_user = {
            "firstName": "Todd",
            "lastName": "Chavez",
            "middleName": "Gustav",
            "email": "todd@pblivin.com",
        }
        self.client_profile_2_user = {
            "firstName": "Mister",
            "lastName": "Peanutbutter",
            "middleName": "Tee",
            "email": "mister@pblivin.com",
        }
        self.client_profile_1_contact_1 = {
            "name": "Jerry",
            "email": "jerry@example.co",
            "phoneNumber": "2125551212",
            "mailingAddress": "1235 Main St",
            "relationshipToClient": RelationshipTypeEnum.OTHER.name,
            "relationshipToClientOther": "bestie",
        }
        self.client_profile_1_contact_2 = {
            "name": "Gary",
            "email": "gary@example.co",
            "phoneNumber": "2125551212",
            "mailingAddress": "1235 Main St",
            "relationshipToClient": RelationshipTypeEnum.CURRENT_CASE_MANAGER.name,
            "relationshipToClientOther": None,
        }
        self.client_profile_2_contact_1 = {
            "name": "Harry",
            "email": "hrry@example.co",
            "phoneNumber": "2125551212",
            "mailingAddress": "1235 Main St",
            "relationshipToClient": RelationshipTypeEnum.CURRENT_CASE_MANAGER.name,
            "relationshipToClientOther": None,
        }
        self.client_1_contacts = [
            self.client_profile_1_contact_1,
            self.client_profile_1_contact_2,
        ]
        self.client_profile_1_hmis_profile_1 = {
            "hmisId": "HMISidLAHSA1",
            "agency": HmisAgencyEnum.LAHSA.name,
        }
        self.client_profile_1_hmis_profile_2 = {
            "hmisId": "HMISidPASADENA1",
            "agency": HmisAgencyEnum.PASADENA.name,
        }
        self.client_1_hmis_profiles = [
            self.client_profile_1_hmis_profile_1,
            self.client_profile_1_hmis_profile_2,
        ]
        self.client_profile_1_household_member_1 = {
            "name": "Daffodil",
            "dateOfBirth": "1900-01-01",
            "gender": GenderEnum.FEMALE.name,
            "relationshipToClient": RelationshipTypeEnum.OTHER.name,
            "relationshipToClientOther": "cartoon friend",
        }
        self.client_profile_1_household_member_2 = {
            "name": "Tulip",
            "dateOfBirth": "1901-01-01",
            "gender": GenderEnum.NON_BINARY.name,
            "relationshipToClient": RelationshipTypeEnum.FRIEND.name,
            "relationshipToClientOther": None,
        }
        self.client_1_household_members = [
            self.client_profile_1_household_member_1,
            self.client_profile_1_household_member_2,
        ]
        self.client_profile_1 = self._create_client_profile_fixture(
            {
                "address": "1475 Luck Hoof Ave, Los Angeles, CA 90046",
                "contacts": self.client_1_contacts,
                "dateOfBirth": self.date_of_birth,
                "eyeColor": EyeColorEnum.BROWN.name,
                "gender": GenderEnum.MALE.name,
                "hairColor": HairColorEnum.BROWN.name,
                "heightInInches": 71.75,
                "hmisId": "HMISidLAHSA0",
                "hmisProfiles": self.client_1_hmis_profiles,
                "householdMembers": self.client_1_household_members,
                "livingSituation": LivingSituationEnum.VEHICLE.name,
                "maritalStatus": MaritalStatusEnum.SINGLE.name,
                "nickname": "Toad",
                "phoneNumber": "2125551212",
                "physicalDescription": "A human",
                "placeOfBirth": "Los Angeles, CA",
                "preferredLanguage": LanguageEnum.ENGLISH.name,
                "pronouns": PronounEnum.HE_HIM_HIS.name,
                "race": RaceEnum.WHITE_CAUCASIAN.name,
                "spokenLanguages": [LanguageEnum.ENGLISH.name, LanguageEnum.SPANISH.name],
                "user": self.client_profile_1_user,
                "veteranStatus": YesNoPreferNotToSayEnum.NO.name,
            }
        )["data"]["createClientProfile"]
        self.client_profile_1_photo_name = self._update_client_profile_photo_fixture(self.client_profile_1["id"])[
            "data"
        ]["updateClientProfilePhoto"]["profilePhoto"]["name"]
        self.client_profile_2 = self._create_client_profile_fixture(
            {
                "address": None,
                "contacts": [],
                "dateOfBirth": None,
                "eyeColor": None,
                "gender": None,
                "hairColor": None,
                "heightInInches": None,
                "hmisId": "HMISidPASADENA2",
                "hmisProfiles": [],
                "householdMembers": [],
                "livingSituation": None,
                "maritalStatus": None,
                "nickname": None,
                "phoneNumber": None,
                "physicalDescription": None,
                "placeOfBirth": None,
                "preferredLanguage": None,
                "pronouns": None,
                "race": None,
                "spokenLanguages": [],
                "user": self.client_profile_2_user,
                "veteranStatus": None,
            }
        )["data"]["createClientProfile"]

    def _setup_client_documents(self) -> None:
        self.client_profile_1_document_1 = self._create_client_document_fixture(
            self.client_profile_1["id"],
            ClientDocumentNamespaceEnum.DRIVERS_LICENSE_FRONT.name,
            b"Client 1 license front",
            "client_profile_1_document_1.txt",
        )["data"]["createClientDocument"]
        self.client_profile_1_document_2 = self._create_client_document_fixture(
            self.client_profile_1["id"],
            ClientDocumentNamespaceEnum.DRIVERS_LICENSE_BACK.name,
            b"Client 1 license back",
            "client_profile_1_document_2.txt",
        )["data"]["createClientDocument"]
        self.client_profile_1_document_3 = self._create_client_document_fixture(
            self.client_profile_1["id"],
            ClientDocumentNamespaceEnum.HMIS_FORM.name,
            b"Client 1 hmis form",
            "client_profile_1_document_3.txt",
        )["data"]["createClientDocument"]
        self.client_profile_1_document_4 = self._create_client_document_fixture(
            self.client_profile_1["id"],
            ClientDocumentNamespaceEnum.OTHER_CLIENT_DOCUMENT.name,
            b"Client 1 other doc",
            "client_profile_1_document_4.txt",
        )["data"]["createClientDocument"]

    def _create_client_profile_fixture(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        return self._create_or_update_client_profile_fixture("create", variables)

    def _update_client_profile_fixture(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        return self._create_or_update_client_profile_fixture("update", variables)

    def _create_or_update_client_profile_fixture(self, operation: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        assert operation in ["create", "update"], "Invalid operation specified."
        mutation: str = f"""
            mutation {operation.capitalize()}ClientProfile($data: {operation.capitalize()}ClientProfileInput!) {{ # noqa: B950
                {operation}ClientProfile(data: $data) {{
                    ... on OperationInfo {{
                        messages {{
                            kind
                            field
                            message
                        }}
                    }}
                    ... on ClientProfileType {{
                        {self.client_profile_fields}
                    }}
                }}
            }}
        """
        return self.execute_graphql(mutation, {"data": variables})

    def _create_client_document_fixture(
        self,
        client_profile_id: str,
        namespace: str,
        file_content: bytes,
        file_name: str = "test_file.txt",
    ) -> Dict[str, Any]:
        file = SimpleUploadedFile(name=file_name, content=file_content)
        response = self.execute_graphql(
            """
            mutation CreateClientDocument($clientProfileId: ID!, $namespace: ClientDocumentNamespaceEnum!, $file: Upload!) {  # noqa: B950
                createClientDocument(data: { clientProfile: $clientProfileId, namespace: $namespace, file: $file }) {
                    ... on OperationInfo {
                        messages {
                            kind
                            field
                            message
                        }
                    }
                    ... on ClientDocumentType {
                        id
                        attachmentType
                        file {
                            name
                        }
                        originalFilename
                        namespace
                    }
                }
            }
            """,
            variables={
                "clientProfileId": client_profile_id,
                "namespace": namespace,
            },
            files={"file": file},
        )
        return response

    def _delete_client_document_fixture(self, document_id: int) -> Dict[str, Any]:
        response = self.execute_graphql(
            """
            mutation DeleteClientDocument($documentId: ID!) {
                deleteClientDocument(data: { id: $documentId }) {
                    ... on OperationInfo {
                        messages {
                            kind
                            field
                            message
                        }
                    }
                    ... on ClientDocumentType {
                        id
                    }
                }
            }
            """,
            variables={"documentId": document_id},
        )
        return response

    def _update_client_profile_photo_fixture(
        self,
        client_profile_id: str,
        photo_content: bytes = b"test photo content",
        photo_name: str = "test_photo.jpg",
    ) -> Dict[str, Any]:
        photo = SimpleUploadedFile(name=photo_name, content=photo_content)

        return self.execute_graphql(
            """
            mutation UpdateClientProfilePhoto($clientProfileId: ID!, $photo: Upload!) {  # noqa: B950
                updateClientProfilePhoto(data: { clientProfile: $clientProfileId, photo: $photo }) {
                    ... on OperationInfo {
                        messages {
                            kind
                            field
                            message
                        }
                    }
                    ... on ClientProfileType {
                        id
                        profilePhoto {
                            name
                        }
                    }
                }
            }
            """,
            variables={
                "clientProfileId": client_profile_id,
            },
            files={"photo": photo},
        )