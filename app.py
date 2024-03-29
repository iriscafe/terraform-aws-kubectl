from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

# Configurações do S3
S3_BUCKET_NAME = 's3-iris'
s3_client = boto3.client('s3')

@app.route('/buckets', methods=['GET'])
def list_buckets():
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return jsonify(buckets)

@app.route('/buckets', methods=['POST'])
def create_bucket():
    bucket_name = request.json.get('bucket_name')
    if not bucket_name:
        return jsonify({'error': 'Nome do bucket não fornecido'}), 400

    try:
        s3_client.create_bucket(Bucket=bucket_name)
        return jsonify({'message': f'Bucket {bucket_name} criado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/buckets/<string:bucket_name>', methods=['DELETE'])
def delete_bucket(bucket_name):
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        return jsonify({'message': f'Bucket {bucket_name} deletado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
