from unittest import skip
from unittest.mock import ANY, patch

import time_machine
from common.models import Address, Location
from django.test import ignore_warnings
from django.utils import timezone
from model_bakery import baker
from notes.enums import DueByGroupEnum, SelahTeamEnum
from notes.models import Mood, Note, ServiceRequest, Task
from notes.tests.utils import (
    NoteGraphQLBaseTestCase,
    ServiceRequestGraphQLBaseTestCase,
    ServiceRequestGraphQLUtilMixin,
    TaskGraphQLBaseTestCase,
    TaskGraphQLUtilsMixin,
)
from unittest_parametrize import parametrize


@ignore_warnings(category=UserWarning)
class NoteMutationTestCase(NoteGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._handle_user_login("org_1_case_manager_1")

    @time_machine.travel("03-12-2024 10:11:12", tick=False)
    def test_create_note_mutation(self) -> None:
        expected_query_count = 37
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_note_fixture(
                {
                    "purpose": "New note purpose",
                    "publicDetails": "New public details",
                    "clientProfile": self.client_profile_1.pk,
                }
            )

        created_note = response["data"]["createNote"]
        expected_note = {
            "id": ANY,
            "purpose": "New note purpose",
            "team": None,
            "location": None,
            "moods": [],
            "purposes": [],
            "nextSteps": [],
            "providedServices": [],
            "requestedServices": [],
            "publicDetails": "New public details",
            "privateDetails": "",
            "isSubmitted": False,
            "clientProfile": {"id": str(self.client_profile_1.pk)},
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "interactedAt": "2024-03-12T10:11:12+00:00",
        }
        self.assertEqual(created_note, expected_note)

    @time_machine.travel("03-12-2024 10:11:12", tick=False)
    def test_update_note_mutation(self) -> None:
        variables = {
            "id": self.note["id"],
            "purpose": "Updated note purpose",
            "team": SelahTeamEnum.WDI_ON_SITE.name,
            "location": self.location.pk,
            "publicDetails": "Updated public details",
            "privateDetails": "Updated private details",
            "isSubmitted": False,
            "interactedAt": "2024-03-12T10:11:12+00:00",
        }

        expected_query_count = 25
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_note_fixture(variables)

        updated_note = response["data"]["updateNote"]
        expected_note = {
            "id": self.note["id"],
            "purpose": "Updated note purpose",
            "team": SelahTeamEnum.WDI_ON_SITE.name,
            "location": {
                "id": str(self.location.pk),
                "address": {
                    "street": self.address.street,
                    "city": self.address.city,
                    "state": self.address.state,
                    "zipCode": self.address.zip_code,
                },
                "point": self.point,
                "pointOfInterest": self.point_of_interest,
            },
            "moods": [],
            "purposes": [],
            "nextSteps": [],
            "providedServices": [],
            "requestedServices": [],
            "publicDetails": "Updated public details",
            "privateDetails": "Updated private details",
            "isSubmitted": False,
            "clientProfile": {"id": str(self.client_profile_1.pk)},
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "interactedAt": "2024-03-12T10:11:12+00:00",
        }
        self.assertEqual(updated_note, expected_note)

    @time_machine.travel("03-12-2024 10:11:12", tick=False)
    def test_partial_update_note_mutation(self) -> None:
        variables = {
            "id": self.note["id"],
            "isSubmitted": True,
            "interactedAt": "2024-03-12T10:11:12+00:00",
        }

        expected_query_count = 22
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_note_fixture(variables)

        updated_note = response["data"]["updateNote"]
        expected_note = {
            "id": self.note["id"],
            "purpose": f"Session with {self.client_profile_1.full_name}",
            "team": None,
            "location": None,
            "moods": [],
            "purposes": [],
            "nextSteps": [],
            "providedServices": [],
            "requestedServices": [],
            "publicDetails": f"{self.client_profile_1.full_name}'s public details",
            "privateDetails": "",
            "isSubmitted": True,
            "clientProfile": {"id": str(self.client_profile_1.pk)},
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "interactedAt": "2024-03-12T10:11:12+00:00",
        }
        self.assertEqual(updated_note, expected_note)

    @skip("not implemented")
    def test_update_note_location_mutation(self) -> None:
        note_id = self.note["id"]
        json_address_input, address_input = self._get_address_inputs()

        location = {
            "address": json_address_input,
            "point": self.point,
            "pointOfInterest": self.point_of_interest,
        }
        variables = {
            "id": note_id,
            "location": location,
        }

        expected_query_count = 25
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_note_location_fixture(variables)

        assert isinstance(address_input["addressComponents"], list)
        expected_address = {
            "street": (
                f"{address_input['addressComponents'][0]['long_name']} "
                f"{address_input['addressComponents'][1]['long_name']}"
            ),
            "city": address_input["addressComponents"][3]["long_name"],
            "state": address_input["addressComponents"][5]["short_name"],
            "zipCode": address_input["addressComponents"][7]["long_name"],
        }

        updated_note_location = response["data"]["updateNoteLocation"]["location"]
        self.assertEqual(updated_note_location["point"], self.point)
        self.assertEqual(updated_note_location["address"], expected_address)

        note = Note.objects.get(id=note_id)
        self.assertIsNotNone(note.location)

        location = Location.objects.get(id=note.location.pk)  # type: ignore
        self.assertEqual(note, location.notes.first())

    @parametrize(
        "task_type, tasks_to_check, expected_query_count",
        [
            ("PURPOSE", "purposes", 36),
            ("NEXT_STEP", "next_steps", 36),
        ],
    )
    @skip("not implemented")
    def test_create_note_task_mutation(
        self,
        task_type: str,
        tasks_to_check: str,
        expected_query_count: int,
    ) -> None:
        variables = {
            "title": "New Note Task",
            "noteId": self.note["id"],
            "status": "TO_DO",
            "taskType": task_type,
        }

        note = Note.objects.get(id=self.note["id"])
        self.assertEqual(getattr(note, tasks_to_check).count(), 0)

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_note_task_fixture(variables)

        expected_task = {
            "id": ANY,
            "title": "New Note Task",
            "status": "TO_DO",
            "dueBy": None,
            "dueByGroup": DueByGroupEnum.NO_DUE_DATE.name,
            "clientProfile": self.note["clientProfile"],
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": ANY,
        }
        created_task = response["data"]["createNoteTask"]

        self.assertEqual(created_task, expected_task)
        self.assertEqual(getattr(note, tasks_to_check).count(), 1)
        self.assertEqual(created_task["id"], str(getattr(note, tasks_to_check).get().id))

    @parametrize(
        "service_request_type, service_requests_to_check, expected_status, expected_query_count",  # noqa E501
        [
            ("REQUESTED", "requested_services", "TO_DO", 34),
            ("PROVIDED", "provided_services", "COMPLETED", 34),
        ],
    )
    def test_create_note_service_request_mutation(
        self,
        service_request_type: str,
        service_requests_to_check: str,
        expected_status: str,
        expected_query_count: int,
    ) -> None:
        variables = {
            "service": "BLANKET",
            "serviceOther": None,
            "noteId": self.note["id"],
            "serviceRequestType": service_request_type,
        }

        note = Note.objects.get(id=self.note["id"])
        self.assertEqual(getattr(note, service_requests_to_check).count(), 0)

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_note_service_request_fixture(variables)

        expected_service_request = {
            "id": ANY,
            "service": "BLANKET",
            "status": expected_status,
            "serviceOther": None,
            "dueBy": None,
            "completedOn": ANY,
            "clientProfile": self.note["clientProfile"],
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": ANY,
        }
        created_service_request = response["data"]["createNoteServiceRequest"]

        self.assertEqual(created_service_request, expected_service_request)
        self.assertEqual(getattr(note, service_requests_to_check).count(), 1)
        self.assertEqual(
            created_service_request["id"],
            str(getattr(note, service_requests_to_check).get().id),
        )

    @parametrize(
        "service_request_type, service_requests_to_check, expected_status, expected_query_count",  # noqa E501
        [
            ("REQUESTED", "requested_services", "TO_DO", 34),
            ("PROVIDED", "provided_services", "COMPLETED", 34),
        ],
    )
    def test_create_note_custom_service_request_mutation(
        self,
        service_request_type: str,
        service_requests_to_check: str,
        expected_status: str,
        expected_query_count: int,
    ) -> None:
        variables = {
            "service": "OTHER",
            "serviceOther": "Other Service",
            "noteId": self.note["id"],
            "serviceRequestType": service_request_type,
        }

        note = Note.objects.get(id=self.note["id"])
        self.assertEqual(getattr(note, service_requests_to_check).count(), 0)

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_note_service_request_fixture(variables)

        expected_service_request = {
            "id": ANY,
            "service": "OTHER",
            "status": expected_status,
            "serviceOther": "Other Service",
            "dueBy": None,
            "completedOn": ANY,
            "clientProfile": self.note["clientProfile"],
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": ANY,
        }
        created_service_request = response["data"]["createNoteServiceRequest"]

        self.assertEqual(created_service_request, expected_service_request)
        self.assertEqual(getattr(note, service_requests_to_check).count(), 1)
        self.assertEqual(
            created_service_request["id"],
            str(getattr(note, service_requests_to_check).get().id),
        )

    @parametrize(
        "service_request_type,  expected_query_count",  # noqa E501
        [
            ("REQUESTED", 10),
            ("PROVIDED", 10),
        ],
    )
    def test_remove_note_service_request_mutation(
        self,
        service_request_type: str,
        expected_query_count: int,
    ) -> None:
        # First create note service request
        variables = {
            "service": "BLANKET",
            "serviceOther": None,
            "noteId": self.note["id"],
            "serviceRequestType": service_request_type,
        }

        created_service_request = self._create_note_service_request_fixture(variables)["data"][
            "createNoteServiceRequest"
        ]

        variables = {
            "serviceRequestId": created_service_request["id"],
            "noteId": self.note["id"],
            "serviceRequestType": service_request_type,
        }

        # Remove note service request
        expected_query_count = expected_query_count
        with self.assertNumQueriesWithoutCache(expected_query_count):
            updated_note = self._remove_note_service_request_fixture(variables)["data"]["removeNoteServiceRequest"]

        self.assertEqual(len(updated_note["requestedServices"]), 0)
        self.assertEqual(len(updated_note["providedServices"]), 0)

    @parametrize(
        "task_type, tasks_to_check",
        [
            ("PURPOSE", "purposes"),
            ("NEXT_STEP", "next_steps"),
        ],
    )
    @skip("not implemented")
    def test_add_note_task_mutation(self, task_type: str, tasks_to_check: str) -> None:
        variables = {
            "noteId": self.note["id"],
            "taskId": self.purpose_1["id"],
            "taskType": task_type,
        }

        note = Note.objects.get(id=self.note["id"])
        self.assertEqual(getattr(note, tasks_to_check).count(), 0)

        expected_query_count = 10
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._add_note_task_fixture(variables)

        expected_note = {
            "id": self.note["id"],
            "purposes": (
                [
                    {"id": self.purpose_1["id"], "title": self.purpose_1["title"]},
                ]
                if tasks_to_check == "purposes"
                else []
            ),
            "nextSteps": (
                [
                    {"id": self.purpose_1["id"], "title": self.purpose_1["title"]},
                ]
                if tasks_to_check == "next_steps"
                else []
            ),
        }
        returned_note = response["data"]["addNoteTask"]
        self.assertEqual(returned_note, expected_note)
        self.assertEqual(1, getattr(note, tasks_to_check).count())
        self.assertEqual(int(self.purpose_1["id"]), getattr(note, tasks_to_check).get().id)

    @parametrize(
        "task_type, tasks_to_check",
        [
            ("PURPOSE", "purposes"),
            ("NEXT_STEP", "next_steps"),
        ],
    )
    @skip("not implemented")
    def test_remove_note_task_mutation(self, task_type: str, tasks_to_check: str) -> None:
        variables = {
            "noteId": self.note["id"],
            "taskId": (self.purpose_1["id"] if tasks_to_check == "purposes" else self.next_step_1["id"]),
            "taskType": task_type,
        }

        note = Note.objects.get(id=self.note["id"])
        note.purposes.add(self.purpose_1["id"])
        note.next_steps.add(self.next_step_1["id"])
        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        expected_query_count = 11
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._remove_note_task_fixture(variables)

        expected_note = {
            "id": self.note["id"],
            "purposes": (
                []
                if tasks_to_check == "purposes"
                else [
                    {"id": str(self.purpose_1["id"]), "title": self.purpose_1["title"]},
                ]
            ),
            "nextSteps": (
                []
                if tasks_to_check == "next_steps"
                else [
                    {
                        "id": self.next_step_1["id"],
                        "title": self.next_step_1["title"],
                    },
                ]
            ),
        }
        returned_note = response["data"]["removeNoteTask"]
        self.assertEqual(returned_note, expected_note)
        self.assertEqual(getattr(note, tasks_to_check).count(), 0)

    def test_create_note_mood_mutation(self) -> None:
        baker.make(Mood, note_id=self.note["id"])
        variables = {
            "descriptor": "ANXIOUS",
            "noteId": self.note["id"],
        }

        note = Note.objects.get(id=self.note["id"])
        self.assertEqual(note.moods.count(), 1)

        expected_query_count = 9
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_note_mood_fixture(variables)

        expected_mood = {
            "id": ANY,
            "descriptor": "ANXIOUS",
        }
        created_mood = response["data"]["createNoteMood"]
        self.assertEqual(created_mood, expected_mood)
        self.assertEqual(note.moods.count(), 2)
        self.assertIn(created_mood["id"], str(note.moods.only("id")))

    def test_delete_mood_mutation(self) -> None:
        note = Note.objects.get(id=self.note["id"])
        moods = baker.make(Mood, note_id=note.id, _quantity=2)
        self.assertEqual(note.moods.count(), 2)

        expected_query_count = 4
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._delete_mood_fixture(mood_id=moods[0].pk)

        self.assertIsNotNone(response["data"]["deleteMood"])
        self.assertEqual(note.moods.count(), 1)
        with self.assertRaises(Mood.DoesNotExist):
            Mood.objects.get(id=moods[0].pk)

    def test_delete_note_mutation(self) -> None:
        mutation = """
            mutation DeleteNote($id: ID!) {
                deleteNote(data: { id: $id }) {
                    ... on OperationInfo {
                        messages {
                            kind
                            field
                            message
                        }
                    }
                    ... on NoteType {
                        id
                    }
                }
            }
        """
        variables = {"id": self.note["id"]}

        expected_query_count = 24
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(mutation, variables)
        self.assertIsNotNone(response["data"]["deleteNote"])

        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=self.note["id"])


class NoteRevertMutationTestCase(NoteGraphQLBaseTestCase, TaskGraphQLUtilsMixin, ServiceRequestGraphQLUtilMixin):
    """
    Asserts that when revertNote mutation is called, the Note instance and all of
    it's related model instances are reverted to their states at the specified moment.
    """

    def setUp(self) -> None:
        super().setUp()
        self._handle_user_login("org_1_case_manager_1")
        self.task_note_fields = """
            purposes {
                id
                title
            }
            nextSteps {
                id
                title
            }
        """
        self.service_note_fields = """
            providedServices {
                id
            }
            requestedServices {
                id
            }
        """

    def test_revert_note_mutation_restores_note_details_to_creation(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Save now as revert_before_timestamp
        2. Update note title, public details, point, and address
        3. Revert to revert_before_timestamp from Step 1
        4. Assert note has details from Step 0
        5. Save now as revert_before_timestamp
        6. Revert to revert_before_timestamp from Step 5
        7. Assert note has details from Step 0
        """
        note_id = self.note["id"]

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        other_address = baker.make(Address, street="Discarded St")
        other_location = baker.make(Location, address=other_address)
        # Update - should be discarded
        self._update_note_fixture(
            {
                "id": note_id,
                "purpose": "Discarded Purpose",
                "publicDetails": "Discarded Body",
                "location": other_location.pk,
            }
        )

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            purpose
            publicDetails
            location {
                id
            }
        """

        expected_query_count = 30
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["purpose"], "Session with Dale Cooper")
        self.assertEqual(reverted_note["publicDetails"], "Dale Cooper's public details")
        self.assertIsNone(reverted_note["location"])

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        expected_query_count = 14
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["purpose"], "Session with Dale Cooper")
        self.assertEqual(reverted_note["publicDetails"], "Dale Cooper's public details")
        self.assertIsNone(reverted_note["location"])

    def test_revert_note_mutation_restores_note_details(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Update note purpose, public details, point, and address
        2. Save now as revert_before_timestamp
        3. Update note purpose, public details, point, and address
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has details from Step 1
        6. Save now as revert_before_timestamp
        7. Revert to revert_before_timestamp from Step 6
        8. Assert note has details from Step 1
        """
        note_id = self.note["id"]

        # Update - should be persisted
        self._update_note_fixture(
            {
                "id": note_id,
                "purpose": "Updated purpose",
                "publicDetails": "Updated Body",
                "location": self.location.pk,
            }
        )

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        other_address = baker.make(Address, street="Discarded St")
        other_location = baker.make(Location, address=other_address)
        # Update - should be discarded
        self._update_note_fixture(
            {
                "id": note_id,
                "purpose": "Discarded purpose",
                "publicDetails": "Discarded Body",
                "location": other_location.pk,
            }
        )

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            purpose
            publicDetails
            location {
                address {
                    street
                }
            }
        """
        expected_query_count = 32
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["purpose"], "Updated purpose")
        self.assertEqual(reverted_note["publicDetails"], "Updated Body")
        self.assertEqual(reverted_note["location"]["address"]["street"], "106 West 1st Street")

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        expected_query_count = 26
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["purpose"], "Updated purpose")
        self.assertEqual(reverted_note["publicDetails"], "Updated Body")
        self.assertEqual(reverted_note["location"]["address"]["street"], "106 West 1st Street")

    def test_revert_note_mutation_reverts_updated_location(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add a location
        2. Save now as revert_before_timestamp
        3. Update the location
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has location from Step 1
        """
        note_id = self.note["id"]
        json_address_input, _ = self._get_address_inputs()

        location = {
            "address": json_address_input,
            "point": self.point,
            "pointOfInterest": self.point_of_interest,
        }
        variables = {
            "id": note_id,
            "location": location,
        }

        # Update - should be persisted
        self._update_note_location_fixture(variables)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        discarded_json_address_input, discarded_address_input = self._get_address_inputs(street_number_override="104")
        discarded_point = [-118.0, 34.0]
        discarded_point_of_interest = "Another interesting point"

        location = {
            "address": discarded_json_address_input,
            "point": discarded_point,
            "pointOfInterest": discarded_point_of_interest,
        }
        variables = {
            "id": note_id,
            "location": location,
        }
        note_fields = """
            location {
                address {
                    street
                }
                point
                pointOfInterest
            }
        """

        # Update - should be discarded
        note_location_to_discard = self._update_note_location_fixture(variables)["data"]["updateNoteLocation"]
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        # Confirm the note location was updated
        self.assertEqual("104 West 1st Street", note_location_to_discard["location"]["address"]["street"])
        self.assertEqual(discarded_point, note_location_to_discard["location"]["point"])
        self.assertEqual(discarded_point_of_interest, note_location_to_discard["location"]["pointOfInterest"])

        expected_query_count = 21
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["location"]["address"]["street"], self.street)
        self.assertEqual(reverted_note["location"]["point"], self.point)
        self.assertEqual(reverted_note["location"]["pointOfInterest"], self.point_of_interest)

    @skip("not implemented")
    def test_revert_note_mutation_removes_added_moods(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 1 mood
        2. Save now as revert_before_timestamp
        3. Add another mood
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only mood from Step 1
        """
        note_id = self.note["id"]

        # Update - should be persisted
        self._create_note_mood_fixture({"descriptor": "ANXIOUS", "noteId": note_id})

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Update - should be discarded
        self._create_note_mood_fixture({"descriptor": "EUTHYMIC", "noteId": note_id})

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            moods {
                descriptor
            }
        """

        expected_query_count = 20
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["moods"]), 1)

    @skip("not implemented")
    def test_revert_note_mutation_returns_removed_moods(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 2 moods
        2. Save now as revert_before_timestamp
        3. Delete 1 mood
        4. Revert to revertBeforeTimestamp from Step 3
        5. Assert note has 2 moods from Step 1
        """
        note_id = self.note["id"]

        # Update - should be persisted
        persisted_mood_variables_1 = {"descriptor": "ANXIOUS", "noteId": note_id}
        self._create_note_mood_fixture(persisted_mood_variables_1)

        persisted_mood_variables_2 = {"descriptor": "EUTHYMIC", "noteId": note_id}
        mood_to_delete_id = self._create_note_mood_fixture(persisted_mood_variables_2)["data"]["createNoteMood"]["id"]

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        self._delete_mood_fixture(mood_id=mood_to_delete_id)

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            moods {
                descriptor
            }
        """

        expected_query_count = 27
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["moods"]), 2)

    @skip("not implemented")
    def test_revert_note_mutation_removes_added_new_tasks(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Create 1 new purpose and 1 new next step
        2. Save now as revert_before_timestamp
        3. Create another purpose and 1 new next step
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)
        total_task_count = Task.objects.count()

        # Add associations that will be persisted
        self._create_note_task_fixture(
            {
                "title": "New Note Purpose",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "PURPOSE",
            }
        )

        self._create_note_task_fixture(
            {
                "title": "New Note Next Step",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Add associations that will be discarded
        self._create_note_task_fixture(
            {
                "title": "Discarded Purpose",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "PURPOSE",
            }
        )

        self._create_note_task_fixture(
            {
                "title": "Discarded Next Step",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 42
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.task_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["purposes"]), 1)
        self.assertEqual(len(reverted_note["nextSteps"]), 1)

        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        # Assert that discarded tasks were deleted
        self.assertEqual(Task.objects.count(), total_task_count + 2)

    @skip("Functionality for adding existing Tasks to a Note is not complete")
    def test_revert_note_mutation_removes_added_existing_tasks(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 1 purpose and 1 next step
        2. Save now as revert_before_timestamp
        3. Add another purpose and next step
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)

        # Add associations that will be persisted
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.purpose_1["id"],
                "taskType": "PURPOSE",
            }
        )
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.next_step_1["id"],
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Add associations that will be discarded
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.purpose_2["id"],
                "taskType": "PURPOSE",
            }
        )
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.next_step_2["id"],
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 27
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.task_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["purposes"]), 1)
        self.assertEqual(len(reverted_note["nextSteps"]), 1)

        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        # Assert that unassociated tasks were not deleted
        self.assertEqual(
            Task.objects.filter(id__in=[self.next_step_2["id"], self.purpose_2["id"]]).count(),
            2,
        )

    def test_revert_note_mutation_removes_added_service_requests(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 1 requested service and 1 provided service
        2. Save now as revert_before_timestamp
        3. Add another requested service and provided service
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)

        # Add associations that will be persisted
        self._create_note_service_request_fixture(
            {
                "service": "BLANKET",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )
        self._create_note_service_request_fixture(
            {
                "service": "WATER",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )
        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Add associations that will be discarded
        discarded_requested_service_id = self._create_note_service_request_fixture(
            {
                "service": "CLOTHES",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )["data"]["createNoteServiceRequest"]["id"]

        discarded_provided_service_id = self._create_note_service_request_fixture(
            {
                "service": "FOOD",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )["data"]["createNoteServiceRequest"]["id"]

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 42
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.service_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["providedServices"]), 1)
        self.assertEqual(len(reverted_note["requestedServices"]), 1)

        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        # Assert that discarded service requests were deleted
        self.assertEqual(
            ServiceRequest.objects.filter(
                id__in=[discarded_requested_service_id, discarded_provided_service_id]
            ).count(),
            0,
        )

    def test_revert_note_mutation_removes_added_custom_service_requests(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 1 custom requested service and 1 custom provided service
        2. Save now as revert_before_timestamp
        3. Add another custom requested service and custom provided service
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)

        # Add associations that will be persisted
        self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Other Service",
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )
        self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Other Service",
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Add associations that will be discarded
        discarded_requested_service_id = self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Discarded Other Service",
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )["data"]["createNoteServiceRequest"]["id"]

        discarded_provided_service_id = self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Discarded Other Service",
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )["data"]["createNoteServiceRequest"]["id"]

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 42
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.service_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["providedServices"]), 1)
        self.assertEqual(len(reverted_note["requestedServices"]), 1)

        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        # Assert that discarded service requests were deleted
        self.assertEqual(
            ServiceRequest.objects.filter(
                id__in=[discarded_requested_service_id, discarded_provided_service_id]
            ).count(),
            0,
        )

    @skip("not implemented")
    def test_revert_note_mutation_returns_removed_new_tasks(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Create 2 new purposes and 2 new next steps
        2. Save now as revert_before_timestamp
        3. Delete 1 purpose and 1 next step
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)
        total_task_count = Task.objects.count()

        # Add associations that will be persisted
        for i in [1, 2]:
            purpose_response = self._create_note_task_fixture(
                {
                    "title": f"New Note Purpose {i}",
                    "noteId": note_id,
                    "status": "TO_DO",
                    "taskType": "PURPOSE",
                }
            )["data"]["createNoteTask"]

            next_step_response = self._create_note_task_fixture(
                {
                    "title": f"New Note Next Step {i}",
                    "noteId": note_id,
                    "status": "TO_DO",
                    "taskType": "NEXT_STEP",
                }
            )["data"]["createNoteTask"]

        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Delete tasks - should be discarded
        self._delete_task_fixture(purpose_response["id"])
        self._delete_task_fixture(next_step_response["id"])

        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 52
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.task_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["purposes"]), 2)
        self.assertEqual(len(reverted_note["nextSteps"]), 2)

        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

        self.assertEqual(Task.objects.count(), total_task_count + 4)

    @skip("Functionality for adding existing Tasks to a Note is not complete")
    def test_revert_note_mutation_returns_removed_existing_tasks(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 2 purposes and 2 next steps
        2. Save now as revert_before_timestamp
        3. Remove 1 purpose and 1 next step
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 1
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)

        # Add associations that will be persisted
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.purpose_1["id"],
                "taskType": "PURPOSE",
            }
        )

        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.next_step_1["id"],
                "taskType": "NEXT_STEP",
            }
        )

        # Add associations that will be removed and then reverted
        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.purpose_2["id"],
                "taskType": "PURPOSE",
            }
        )

        self._add_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.next_step_2["id"],
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Remove task - should be discarded
        self._remove_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.purpose_2["id"],
                "taskType": "PURPOSE",
            }
        )

        self._remove_note_task_fixture(
            {
                "noteId": note_id,
                "taskId": self.next_step_2["id"],
                "taskType": "NEXT_STEP",
            }
        )
        self.assertEqual(note.purposes.count(), 1)
        self.assertEqual(note.next_steps.count(), 1)

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 27
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.task_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["purposes"]), 2)
        self.assertEqual(len(reverted_note["nextSteps"]), 2)

        self.assertEqual(note.purposes.count(), 2)
        self.assertEqual(note.next_steps.count(), 2)

    def test_revert_note_mutation_returns_removed_service_requests(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 2 requested service and 2 provided service
        2. Save now as revert_before_timestamp
        3. Remove 1 requested service and 1 provided service
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 1
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)
        total_service_request_count = ServiceRequest.objects.count()

        # Add associations that will be persisted
        self._create_note_service_request_fixture(
            {
                "service": "BLANKET",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )
        self._create_note_service_request_fixture(
            {
                "service": "WATER",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )
        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        # Add associations that will be removed and then reverted
        reverted_requested_service = self._create_note_service_request_fixture(
            {
                "service": "CLOTHES",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )["data"]["createNoteServiceRequest"]

        reverted_provided_service = self._create_note_service_request_fixture(
            {
                "service": "FOOD",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )["data"]["createNoteServiceRequest"]

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Delete service requests - should be discarded
        self._delete_service_request_fixture(reverted_provided_service["id"])
        self._delete_service_request_fixture(reverted_requested_service["id"])

        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 50
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.service_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["providedServices"]), 2)
        self.assertEqual(len(reverted_note["requestedServices"]), 2)

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        self.assertEqual(ServiceRequest.objects.count(), total_service_request_count + 4)

    def test_revert_note_mutation_returns_removed_custom_service_requests(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Add 2 custom requested service and 2 custom provided service
        2. Save now as revert_before_timestamp
        3. Remove 1 custom requested service and 1 custom provided service
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 1
        """
        note_id = self.note["id"]
        note = Note.objects.get(id=note_id)
        total_service_request_count = ServiceRequest.objects.count()

        # Add associations that will be persisted
        self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Other Service",
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )
        self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Other Service",
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )

        # Add associations that will be removed and then reverted
        reverted_requested_service = self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Retrieved Other Service",
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )["data"]["createNoteServiceRequest"]

        reverted_provided_service = self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Retrieved Other Service",
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )["data"]["createNoteServiceRequest"]

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Delete service requests - should be discarded
        self._delete_service_request_fixture(reverted_provided_service["id"])
        self._delete_service_request_fixture(reverted_requested_service["id"])

        self.assertEqual(note.provided_services.count(), 1)
        self.assertEqual(note.requested_services.count(), 1)

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 50
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.service_note_fields)["data"]["revertNote"]

        self.assertEqual(len(reverted_note["providedServices"]), 2)
        self.assertEqual(len(reverted_note["requestedServices"]), 2)

        self.assertEqual(note.provided_services.count(), 2)
        self.assertEqual(note.requested_services.count(), 2)

        self.assertEqual(ServiceRequest.objects.count(), total_service_request_count + 4)

    @skip("not implemented")
    def test_revert_note_mutation_restores_updated_tasks(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Create 1 purpose and 1 next step
        2. Save now as revert_before_timestamp
        3. Update the purpose and next step titles
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]

        # Add associations that will be persisted
        purpose = self._create_note_task_fixture(
            {
                "title": "Purpose Title",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "PURPOSE",
            }
        )["data"]["createNoteTask"]

        next_step = self._create_note_task_fixture(
            {
                "title": "Next Step Title",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "NEXT_STEP",
            }
        )["data"]["createNoteTask"]

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Make updates that will be discarded
        self._update_task_fixture({"id": purpose["id"], "title": "Discarded Purpose Title"})
        self._update_task_fixture({"id": next_step["id"], "title": "Discarded Next Step Title"})

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}

        expected_query_count = 24
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, self.task_note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["purposes"][0]["title"], "Purpose Title")
        self.assertEqual(reverted_note["nextSteps"][0]["title"], "Next Step Title")

    @skip("not implemented")
    def test_revert_note_mutation_restores_updated_task_location(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Create 1 next step
        2. Update next step location
        3. Save now as revert_before_timestamp
        3. Update the next step location again
        4. Revert to revert_before_timestamp from Step 3
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]

        task = self._create_note_task_fixture(
            {
                "title": "Next Step Title",
                "noteId": note_id,
                "status": "TO_DO",
                "taskType": "NEXT_STEP",
            }
        )["data"]["createNoteTask"]

        json_address_input, address_input = self._get_address_inputs()
        location = {
            "address": json_address_input,
            "point": self.point,
            "pointOfInterest": self.point_of_interest,
        }

        self._update_task_location_fixture({"id": task["id"], "location": location})

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        discarded_json_address_input, discarded_address_input = self._get_address_inputs(street_number_override="104")
        discarded_point = [-118.0, 34.0]
        discarded_point_of_interest = "Another interesting point"
        discarded_location = {
            "address": discarded_json_address_input,
            "point": discarded_point,
            "pointOfInterest": discarded_point_of_interest,
        }
        self._update_task_location_fixture({"id": task["id"], "location": discarded_location})

        # Revert to revert_before_timestamp state
        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            nextSteps {
                id
                title
                location {
                    address {
                        street
                        city
                        state
                        zipCode
                    }
                    point
                    pointOfInterest
                }
            }
        """

        expected_query_count = 20
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        next_step = reverted_note["nextSteps"][0]
        self.assertEqual(next_step["location"]["address"]["street"], self.street)
        self.assertEqual(next_step["location"]["point"], self.point)
        self.assertEqual(next_step["location"]["pointOfInterest"], self.point_of_interest)

    @skip("not implemented")
    def test_revert_note_mutation_restores_updated_custom_service_requests(self) -> None:
        """
        Test Actions:
        0. Setup creates a note
        1. Create 1 custom service request and 1 custom provided service
        2. Save now as revert_before_timestamp
        3. Update the service request and provided service titles
        4. Revert to revert_before_timestamp from Step 2
        5. Assert note has only the associations from Step 2
        """
        note_id = self.note["id"]

        # Add associations that will be persisted
        provided_service = self._create_note_service_request_fixture(
            {
                "service": "OTHER",
                "serviceOther": "Other Provided Service",
                "noteId": note_id,
                "serviceRequestType": "PROVIDED",
            }
        )["data"]["createNoteServiceRequest"]

        requested_service = self._create_note_service_request_fixture(
            {
                "service": "BLANKET",
                "serviceOther": None,
                "noteId": note_id,
                "serviceRequestType": "REQUESTED",
            }
        )["data"]["createNoteServiceRequest"]

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Make updates that will be discarded
        self._update_service_request_fixture(
            {
                "id": provided_service["id"],
                "serviceOther": "Discarded Provided Service Title",
            }
        )
        self._update_service_request_fixture(
            {
                "id": requested_service["id"],
                "dueBy": "2024-03-11T11:12:13+00:00",
                "status": "COMPLETED",
            }
        )

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            providedServices {
                id
                serviceOther
            }
            requestedServices {
                id
                status
                dueBy
            }
        """

        expected_query_count = 24
        with self.assertNumQueriesWithoutCache(expected_query_count):
            reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(reverted_note["providedServices"][0]["serviceOther"], "Other Provided Service")
        self.assertEqual(reverted_note["requestedServices"][0]["status"], "TO_DO")
        self.assertEqual(reverted_note["requestedServices"][0]["dueBy"], None)

    def test_revert_note_mutation_fails_in_atomic_transaction(self) -> None:
        """
        Asserts that when revertNote mutation fails, the Note instance is not partially updated.
        """
        note_id = self.note["id"]
        self._update_note_fixture({"id": note_id, "purpose": "Updated Purpose"})

        # Select a moment to revert to
        revert_before_timestamp = timezone.now()

        # Update - should be persisted because revert fails
        self._update_note_fixture({"id": note_id, "purpose": "Discarded Purpose"})
        self._create_note_mood_fixture({"descriptor": "ANXIOUS", "noteId": note_id})

        variables = {"id": note_id, "revertBeforeTimestamp": revert_before_timestamp}
        note_fields = """
            purpose
            moods {
                descriptor
            }
        """

        with patch("notes.models.Mood.revert_action", side_effect=Exception("oops")):
            not_reverted_note = self._revert_note_fixture(variables, note_fields)["data"]["revertNote"]

        self.assertEqual(len(not_reverted_note["moods"]), 1)
        self.assertEqual(not_reverted_note["purpose"], "Discarded Purpose")


@skip("Service Requests are not currently implemented")
@ignore_warnings(category=UserWarning)
@time_machine.travel("2024-03-11 10:11:12", tick=False)
class ServiceRequestMutationTestCase(ServiceRequestGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._handle_user_login("org_1_case_manager_1")

    def test_create_service_request_mutation(self) -> None:
        expected_query_count = 29
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_service_request_fixture(
                {
                    "service": "BLANKET",
                    "status": "TO_DO",
                }
            )
        created_service_request = response["data"]["createServiceRequest"]
        expected_service_request = {
            "id": ANY,
            "service": "BLANKET",
            "serviceOther": None,
            "dueBy": None,
            "completedOn": None,
            "status": "TO_DO",
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-03-11T10:11:12+00:00",
        }
        self.assertEqual(created_service_request, expected_service_request)

    @time_machine.travel("2024-03-11 12:34:56", tick=False)
    def test_update_service_request_mutation(self) -> None:
        variables = {
            "id": self.service_request["id"],
            "dueBy": "2024-03-11T11:12:13+00:00",
            "status": "COMPLETED",
        }

        expected_query_count = 15
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_service_request_fixture(variables)

        updated_service_request = response["data"]["updateServiceRequest"]
        expected_service_request = {
            "id": self.service_request["id"],
            "service": "BLANKET",
            "serviceOther": None,
            "status": "COMPLETED",
            "dueBy": "2024-03-11T11:12:13+00:00",
            "completedOn": "2024-03-11T12:34:56+00:00",
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-03-11T10:11:12+00:00",
        }
        self.assertEqual(updated_service_request, expected_service_request)

    @time_machine.travel("2024-03-11 12:34:56", tick=False)
    def test_partial_update_service_request_mutation(self) -> None:
        variables = {
            "id": self.service_request["id"],
        }

        expected_query_count = 15
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_service_request_fixture(variables)

        updated_service_request = response["data"]["updateServiceRequest"]
        expected_service_request = {
            "id": self.service_request["id"],
            "service": "BLANKET",
            "serviceOther": None,
            "status": "TO_DO",
            "dueBy": None,
            "completedOn": None,
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-03-11T10:11:12+00:00",
        }
        self.assertEqual(updated_service_request, expected_service_request)

    def test_delete_service_request_mutation(self) -> None:
        mutation = """
            mutation DeleteServiceRequest($id: ID!) {
                deleteServiceRequest(data: { id: $id }) {
                    ... on OperationInfo {
                        messages {
                            kind
                            field
                            message
                        }
                    }
                    ... on DeletedObjectType {
                        id
                    }
                }
            }
        """
        variables = {"id": self.service_request["id"]}

        expected_query_count = 10
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(mutation, variables)

        self.assertIsNotNone(response["data"]["deleteServiceRequest"])

        with self.assertRaises(ServiceRequest.DoesNotExist):
            ServiceRequest.objects.get(id=self.service_request["id"])


@skip("Tasks are not currently implemented")
@ignore_warnings(category=UserWarning)
@time_machine.travel("2024-02-26T10:11:12+00:00", tick=False)
class TaskMutationTestCase(TaskGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._handle_user_login("org_1_case_manager_1")

    def test_create_task_mutation(self) -> None:
        expected_query_count = 29
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._create_task_fixture(
                {
                    "title": "New Task",
                    "status": "TO_DO",
                }
            )
        created_task = response["data"]["createTask"]
        expected_task = {
            "id": ANY,
            "title": "New Task",
            "location": None,
            "status": "TO_DO",
            "dueBy": None,
            "dueByGroup": DueByGroupEnum.NO_DUE_DATE.name,
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-02-26T10:11:12+00:00",
        }
        self.assertEqual(created_task, expected_task)

    def test_update_task_mutation(self) -> None:
        variables = {
            "id": self.task["id"],
            "title": "Updated task title",
            "location": self.location.pk,
            "status": "COMPLETED",
        }

        expected_query_count = 18
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_task_fixture(variables)
        updated_task = response["data"]["updateTask"]
        expected_task = {
            "id": self.task["id"],
            "title": "Updated task title",
            "location": {
                "id": str(self.location.pk),
                "address": {
                    "street": self.address.street,
                    "city": self.address.city,
                    "state": self.address.state,
                    "zipCode": self.address.zip_code,
                },
                "point": self.point,
                "pointOfInterest": self.point_of_interest,
            },
            "status": "COMPLETED",
            "dueBy": None,
            "dueByGroup": DueByGroupEnum.NO_DUE_DATE.name,
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-02-26T10:11:12+00:00",
        }
        self.assertEqual(updated_task, expected_task)

    def test_partial_update_task_mutation(self) -> None:
        variables = {
            "id": self.task["id"],
            "title": "Updated task title",
        }

        expected_query_count = 15
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_task_fixture(variables)
        updated_task = response["data"]["updateTask"]
        expected_task = {
            "id": self.task["id"],
            "title": "Updated task title",
            "location": None,
            "status": "TO_DO",
            "dueBy": None,
            "dueByGroup": DueByGroupEnum.NO_DUE_DATE.name,
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-02-26T10:11:12+00:00",
        }
        self.assertEqual(updated_task, expected_task)

    def test_update_task_location_mutation(self) -> None:
        task_id = self.task["id"]
        json_address_input, address_input = self._get_address_inputs()
        location = {
            "address": json_address_input,
            "point": self.point,
            "pointOfInterest": self.point_of_interest,
        }
        variables = {
            "id": task_id,
            "location": location,
        }

        expected_query_count = 23
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._update_task_location_fixture(variables)

        assert isinstance(address_input["addressComponents"], list)
        expected_address = {
            "street": (
                f"{address_input['addressComponents'][0]['long_name']} "
                f"{address_input['addressComponents'][1]['long_name']}"
            ),
            "city": address_input["addressComponents"][3]["long_name"],
            "state": address_input["addressComponents"][5]["short_name"],
            "zipCode": address_input["addressComponents"][7]["long_name"],
        }
        expected_location = {
            "id": ANY,
            "address": expected_address,
            "point": self.point,
            "pointOfInterest": self.point_of_interest,
        }
        updated_task_location = response["data"]["updateTaskLocation"]["location"]
        self.assertEqual(updated_task_location, expected_location)

        task = Task.objects.get(id=task_id)
        self.assertIsNotNone(task.location)

        location = Location.objects.get(id=task.location.pk)  # type: ignore
        self.assertEqual(task, location.tasks.first())

    def test_delete_task_mutation(self) -> None:
        expected_query_count = 10
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self._delete_task_fixture(self.task["id"])

        self.assertIsNotNone(response["data"]["deleteTask"])
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task["id"])
