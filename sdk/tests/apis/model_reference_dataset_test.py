import unittest
import uuid
import responses
from radicalbit_platform_sdk.apis import ModelReferenceDataset
from radicalbit_platform_sdk.models import ReferenceFileUpload, ModelType, JobStatus
from radicalbit_platform_sdk.errors import ClientError

class ModelReferenceDatasetTest(unittest.TestCase):

    @responses.activate
    def test_statistics_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        n_variables = 10
        n_observations = 1000
        missing_cells = 10
        missing_cells_perc = 1
        duplicate_rows = 10
        duplicate_rows_perc = 1
        numeric = 3
        categorical = 6
        datetime = 1

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/statistics',
            status=200,
            json={
                'datetime': 'something_not_used',
                'jobStatus': 'SUCCEEDED',
                'statistics': {
                    'nVariables': n_variables,
                    'nObservations': n_observations,
                    'missingCells': missing_cells,
                    'missingCellsPerc': missing_cells_perc,
                    'duplicateRows': duplicate_rows,
                    'duplicateRowsPerc': duplicate_rows_perc,
                    'numeric': numeric,
                    'categorical': categorical,
                    'datetime': datetime
                }
            },
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        stats = model_reference_dataset.statistics()

        self.assertEqual(stats.n_variables, n_variables)
        self.assertEqual(stats.n_observations, n_observations)
        self.assertEqual(stats.missing_cells, missing_cells)
        self.assertEqual(stats.missing_cells_perc, missing_cells_perc)
        self.assertEqual(stats.duplicate_rows, duplicate_rows)
        self.assertEqual(stats.duplicate_rows_perc, duplicate_rows_perc)
        self.assertEqual(stats.numeric, numeric)
        self.assertEqual(stats.categorical, categorical)
        self.assertEqual(stats.datetime, datetime)
        self.assertEqual(model_reference_dataset.status(), JobStatus.SUCCEEDED)

    @responses.activate
    def test_statistics_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/statistics',
            status=200,
            json={'statistics': 'wrong'},
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.statistics()

    @responses.activate
    def test_statistics_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/statistics',
            status=200,
            json={'wrong': 'json'},
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.statistics()

    @responses.activate
    def test_model_metrics_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        f1 = 0.75
        accuracy = 0.98
        recall = 0.15
        weighted_precision = 4.22
        weighted_recall = 9.33
        weighted_true_positive_rate = 4.12
        weighted_false_positive_rate = 5.89
        weighted_f_measure = 32.9
        true_positive_rate = 32.9
        false_positive_rate = 4.12
        area_under_roc = 45.2
        area_under_pr = 32.9
        true_positive_count = 10
        false_positive_count = 5
        true_negative_count = 2
        false_negative_count = 7

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/model-quality',
            status=200,
            json={
                'datetime': 'something_not_used',
                'jobStatus': 'SUCCEEDED',
                'modelQuality': {
                    'f1': f1,
                    'accuracy': accuracy,
                    'precision': recall,
                    'recall': recall,
                    'fMeasure': weighted_f_measure,
                    'weightedPrecision': weighted_precision,
                    'weightedRecall': weighted_recall,
                    'weightedFMeasure': weighted_f_measure,
                    'weightedTruePositiveRate': weighted_true_positive_rate,
                    'weightedFalsePositiveRate': weighted_false_positive_rate,
                    'truePositiveRate': true_positive_rate,
                    'falsePositiveRate': false_positive_rate,
                    'areaUnderRoc': area_under_roc,
                    'areaUnderPr': area_under_pr,
                    'truePositiveCount': true_positive_count,
                    'falsePositiveCount': false_positive_count,
                    'trueNegativeCount': true_negative_count,
                    'falseNegativeCount': false_negative_count
                }
            },
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        metrics = model_reference_dataset.model_quality()

        self.assertEqual(metrics.f1, f1)
        self.assertEqual(metrics.accuracy, accuracy)
        self.assertEqual(metrics.recall, recall)
        self.assertEqual(metrics.weighted_precision, weighted_precision)
        self.assertEqual(metrics.weighted_recall, weighted_recall)
        self.assertEqual(metrics.weighted_true_positive_rate, weighted_true_positive_rate)
        self.assertEqual(metrics.weighted_false_positive_rate, weighted_false_positive_rate)
        self.assertEqual(metrics.weighted_f_measure, weighted_f_measure)
        self.assertEqual(metrics.true_positive_rate, true_positive_rate)
        self.assertEqual(metrics.false_positive_rate, false_positive_rate)
        self.assertEqual(metrics.true_positive_count, true_positive_count)
        self.assertEqual(metrics.false_positive_count, false_positive_count)
        self.assertEqual(metrics.true_negative_count, true_negative_count)
        self.assertEqual(metrics.false_negative_count, false_negative_count)
        self.assertEqual(model_reference_dataset.status(), JobStatus.SUCCEEDED)

    @responses.activate
    def test_model_metrics_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/model-quality',
            status=200,
            json={'modelQuality': 'wrong'},
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.model_quality()

    @responses.activate
    def test_model_metrics_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()

        responses.add(
            responses.GET,
            f'{base_url}/api/models/{str(model_id)}/reference/model-quality',
            status=200,
            json={'wrong': 'json'},
        )

        model_reference_dataset = ModelReferenceDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            ReferenceFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.model_quality()
