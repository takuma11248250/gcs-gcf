from google.cloud import bigquery

def load_data(data, context):
    client = bigquery.Client()
    project_id = 'causal-temple-316609'
    dataset_id = 'gcs_gcf'

    bucket_name = data['bucket']
    file_name = data['name']
    file_ext = file_name.split('.')[-1]

    if file_ext == 'csv':
        uri = 'gs://' + bucket_name + '/' + file_name
        table_id = 'import_data'
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        #load config
        job_config = bigquery.LoadJobConfig()
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV

        #load data
        load_job = client.load_table_from_uri(
            uri,
            table_ref,
            job_config=job_config
        )
        print('Started job {}'.format(load_job.job_id))
        load_job.result()
        print('Job finished.')
        destination_table = client.get_table(dataset_ref.table(table_id))
        print('Loaded {} rows.'.format(destination_table.num_rows))

    else:
        print('Nothing To Do')