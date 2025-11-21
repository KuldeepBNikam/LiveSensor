class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:

            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)
            
            logging.info("Starting data ingestion")

            
