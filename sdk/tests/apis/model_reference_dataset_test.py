import unittest
import uuid
import responses
from radicalbit_platform_sdk.apis import ModelReferenceDataset
from radicalbit_platform_sdk.models import ReferenceFileUpload, ModelType, JobStatus
from radicalbit_platform_sdk.errors import ClientError

class ModelReferenceDatasetTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://api:9000'
        self.model_id = uuid.uuid4()
        self.import_uuid = uuid.uuid4()
        self.model_reference_dataset = ModelReferenceDataset(
            self.base_url,
            self.model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=self.import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

    @responses.activate
    def test_statistics_ok(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/statistics',
            status=200,
            json={
                'datetime': 'something_not_used',
                'jobStatus': 'SUCCEEDED',
                'statistics': {
                    'nVariables': 10,
                    'nObservations': 1000,
                    'missingCells': 10,
                    'missingCellsPerc': 1,
                    'duplicateRows': 10,
                    'duplicateRowsPerc': 1,
                    'numeric': 3,
                    'categorical': 6,
                    'datetime': 1
                }
            },
        )
        stats = self.model_reference_dataset.statistics()
        self.assertEqual(stats.n_variables, 10)
        self.assertEqual(stats.n_observations, 1000)
        self.assertEqual(stats.missing_cells, 10)
        self.assertEqual(stats.missing_cells_perc, 1)
        self.assertEqual(stats.duplicate_rows, 10)
        self.assertEqual(stats.duplicate_rows_perc, 1)
        self.assertEqual(stats.numeric, 3)
        self.assertEqual(stats.categorical, 6)
        self.assertEqual(stats.datetime, 1)
        self.assertEqual(self.model_reference_dataset.status(), JobStatus.SUCCEEDED)

    @responses.activate
    def test_statistics_validation_error(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/statistics',
            status=200,
            json={'statistics': 'wrong'},
        )
        with self.assertRaises(ClientError):
            self.model_reference_dataset.statistics()

    @responses.activate
    def test_statistics_key_error(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/statistics',
            status=200,
            json={'wrong': 'json'},
        )
        with self.assertRaises(ClientError):
            self.model_reference_dataset.statistics()

    @responses.activate
    def test_model_metrics_ok(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/model-quality',
            status=200,
            json={
                'datetime': 'something_not_used',
                'jobStatus': 'SUCCEEDED',
                'modelQuality': {
                    'f1': 0.75,
                    'accuracy': 0.98,
                    'precision': 0.23,
                    'recall': 0.15,
                    'fMeasure': 2.45,
                    'weightedPrecision': 4.22,
                    'weightedRecall': 9.33,
                    'weightedFMeasure': 32.9,
                    'weightedTruePositiveRate': 4.12,
                    'weightedFalsePositiveRate': 5.89,
                    'truePositiveRate': 32.9,
                    'falsePositiveRate': 4.12,
                    'areaUnderRoc': 45.2,
                    'areaUnderPr': 32.9,
                    'truePositiveCount': 10,
                    'falsePositiveCount': 5,
                    'trueNegativeCount': 2,
                    'falseNegativeCount': 7
                }
            },
        )
        metrics = self.model_reference_dataset.model_quality()
        self.assertEqual(metrics.f1, 0.75)
        self.assertEqual(metrics.accuracy, 0.98)
        self.assertEqual(metrics.recall, 0.15)
        self.assertEqual(metrics.weighted_precision, 4.22)
        self.assertEqual(metrics.weighted_recall, 9.33)
        self.assertEqual(metrics.weighted_true_positive_rate, 4.12)
        self.assertEqual(metrics.weighted_false_positive_rate, 5.89)
        self.assertEqual(metrics.weighted_f_measure, 32.9)
        self.assertEqual(metrics.true_positive_rate, 32.9)
        self.assertEqual(metrics.false_positive_rate, 4.12)
        self.assertEqual(metrics.true_positive_count, 10)
        self.assertEqual(metrics.false_positive_count, 5)
        self.assertEqual(metrics.true_negative_count, 2)
        self.assertEqual(metrics.false_negative_count, 7)
        self.assertEqual(metrics.precision, 0.23)
        self.assertEqual(metrics.f_measure, 2.45)
        self.assertEqual(metrics.area_under_roc, 45.2)
        self.assertEqual(metrics.area_under_pr, 32.9)
        self.assertEqual(self.model_reference_dataset.status(), JobStatus.SUCCEEDED)

    @responses.activate
    def test_model_metrics_validation_error(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/model-quality',
            status=200,
            json={'modelQuality': 'wrong'},
        )
        with self.assertRaises(ClientError):
            self.model_reference_dataset.model_quality()

    @responses.activate
    def test_model_metrics_key_error(self):
        responses.add(
            responses.GET,
            f'{self.base_url}/api/models/{str(self.model_id)}/reference/model-quality',
            status=200,
            json={'wrong': 'json'},
        )
        with self.assertRaises(ClientError):
            self.model_reference_dataset.model_quality()