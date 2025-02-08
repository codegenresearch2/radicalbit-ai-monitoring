from radicalbit_platform_sdk.apis import ModelReferenceDataset\"nfrom radicalbit_platform_sdk.models import ReferenceFileUpload, ModelType, JobStatus\"nfrom radicalbit_platform_sdk.errors import ClientError\"nimport responses\"nimport unittest\"nimport uuid\"n\n\nclass ModelReferenceDatasetTest(unittest.TestCase):\n    @responses.activate\n    def test_statistics_ok(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        n_variables = 10\n        n_observations = 1000\n        missing_cells = 10\n        missing_cells_perc = 1\n        duplicate_rows = 10\n        duplicate_rows_perc = 1\n        numeric = 3\n        categorical = 6\n        datetime = 1\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/statistics",\n                "status": 200,\n                "body": f"{{\n                    \"datetime\": \"something_not_used\",\n                    \"jobStatus\": \"SUCCEEDED\",\n                    \"statistics\": {{ \n                        \"nVariables\": {n_variables},\n                        \"nObservations\": {n_observations},\n                        \"missingCells\": {missing_cells},\n                        \"missingCellsPerc\": {missing_cells_perc},\n                        \"duplicateRows\": {duplicate_rows},\n                        \"duplicateRowsPerc\": {duplicate_rows_perc},\n                        \"numeric\": {numeric},\n                        \"categorical\": {categorical},\n                        \"datetime\": {datetime} \n                    }} \n                }}"\n            }\n        )\n\n        stats = model_reference_dataset.statistics()\n\n        assert stats.n_variables == {n_variables}\n        assert stats.n_observations == {n_observations}\n        assert stats.missing_cells == {missing_cells}\n        assert stats.missing_cells_perc == {missing_cells_perc}\n        assert stats.duplicate_rows == {duplicate_rows}\n        assert stats.duplicate_rows_perc == {duplicate_rows_perc}\n        assert stats.numeric == {numeric}\n        assert stats.categorical == {categorical}\n        assert stats.datetime == {datetime}\n        assert model_reference_dataset.status() == JobStatus.SUCCEEDED\n\n    @responses.activate\n    def test_statistics_validation_error(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/statistics",\n                "status": 200,\n                "body": '{\"statistics\": \"wrong\"}',\n            }\n        )\n\n        with self.assertRaises(ClientError):\n            model_reference_dataset.statistics()\n\n    @responses.activate\n    def test_statistics_key_error(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/statistics",\n                "status": 200,\n                "body": '{\"wrong\": \"json\"}',\n            }\n        )\n\n        with self.assertRaises(ClientError):\n            model_reference_dataset.statistics()\n\n    @responses.activate\n    def test_model_metrics_ok(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        f1 = 0.75\n        accuracy = 0.98\n        recall = 0.23\n        weighted_precision = 0.15\n        weighted_true_positive_rate = 0.01\n        weighted_false_positive_rate = 0.23\n        weighted_f_measure = 2.45\n        true_positive_rate = 4.12\n        false_positive_rate = 5.89\n        precision = 2.33\n        weighted_recall = 4.22\n        f_measure = 9.33\n        area_under_roc = 45.2\n        area_under_pr = 32.9\n        true_positive_count = 10\n        false_positive_count = 5\n        true_negative_count = 2\n        false_negative_count = 7\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/model-quality",\n                "status": 200,\n                "body": f"{{\n                    \"datetime\": \"something_not_used\",\n                    \"jobStatus\": \"SUCCEEDED\",\n                    \"modelQuality\": {{ \n                        \"f1\": {f1},\n                        \"accuracy\": {accuracy},\n                        \"precision\": {precision},\n                        \"recall\": {recall},\n                        \"fMeasure\": {f_measure},\n                        \"weightedPrecision\": {weighted_precision},\n                        \"weightedRecall\": {weighted_recall},\n                        \"weightedFMeasure\": {weighted_f_measure},\n                        \"weightedTruePositiveRate\": {weighted_true_positive_rate},\n                        \"weightedFalsePositiveRate\": {weighted_false_positive_rate},\n                        \"truePositiveRate\": {true_positive_rate},\n                        \"falsePositiveRate\": {false_positive_rate},\n                        \"areaUnderRoc\": {area_under_roc},\n                        \"areaUnderPr\": {area_under_pr},\n                        \"truePositiveCount\": {true_positive_count},\n                        \"falsePositiveCount\": {false_positive_count},\n                        \"trueNegativeCount\": {true_negative_count},\n                        \"falseNegativeCount\": {false_negative_count} \n                    }} \n                }}"\n            }\n        )\n\n        metrics = model_reference_dataset.model_quality()\n\n        assert metrics.f1 == {f1}\n        assert metrics.accuracy == {accuracy}\n        assert metrics.recall == {recall}\n        assert metrics.weighted_precision == {weighted_precision}\n        assert metrics.weighted_recall == {weighted_recall}\n        assert metrics.weighted_true_positive_rate == {weighted_true_positive_rate}\n        assert metrics.weighted_false_positive_rate == {weighted_false_positive_rate}\n        assert metrics.weighted_f_measure == {weighted_f_measure}\n        assert metrics.true_positive_rate == {true_positive_rate}\n        assert metrics.false_positive_rate == {false_positive_rate}\n        assert metrics.true_positive_count == {true_positive_count}\n        assert metrics.false_positive_count == {false_positive_count}\n        assert metrics.true_negative_count == {true_negative_count}\n        assert metrics.false_negative_count == {false_negative_count}\n        assert metrics.precision == {precision}\n        assert metrics.f_measure == {f_measure}\n        assert metrics.area_under_roc == {area_under_roc}\n        assert metrics.area_under_pr == {area_under_pr}\n        assert model_reference_dataset.status() == JobStatus.SUCCEEDED\n\n    @responses.activate\n    def test_model_metrics_validation_error(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/model-quality",\n                "status": 200,\n                "body": '{\"modelQuality\": \"wrong\"}',\n            }\n        )\n\n        with self.assertRaises(ClientError):\n            model_reference_dataset.model_quality()\n\n    @responses.activate\n    def test_model_metrics_key_error(self):\n        base_url = "http://api:9000"\n        model_id = uuid.uuid4()\n        import_uuid = uuid.uuid4()\n        model_reference_dataset = ModelReferenceDataset(\n            base_url,\n            model_id,\n            ModelType.BINARY,\n            ReferenceFileUpload(\n                uuid=import_uuid,\n                path="s3://bucket/file.csv",\n                date="2014",\n                status=JobStatus.IMPORTING,\n            ),\n        )\n\n        responses.add(\n            **{\n                "method": responses.GET,\n                "url": f"{base_url}/api/models/{str(model_id)}/reference/model-quality",\n                "status": 200,\n                "body": '{\"wrong\": \"json\"}',\n            }\n        )\n\n        with self.assertRaises(ClientError):\n            model_reference_dataset.model_quality()\n