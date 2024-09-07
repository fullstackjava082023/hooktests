from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        
        # Check if the event is a merged pull request
        if payload['action'] == 'closed' and payload['pull_request']['merged']:
            repo_name = payload['repository']['full_name']
            pr_number = payload['pull_request']['number']
            
            # Get the list of files changed in the pull request
            files_url = payload['pull_request']['url'] + '/files'
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': f'token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN'
            }
            
            response = request.get(files_url, headers=headers)
            files_changed = response.json()
            
            added_files = [file['filename'] for file in files_changed if file['status'] == 'added']
            modified_files = [file['filename'] for file in files_changed if file['status'] == 'modified']
            removed_files = [file['filename'] for file in files_changed if file['status'] == 'removed']
            
            # Log the repository name and changed files
            logger.info(f'Repository: {repo_name}')
            logger.info(f'Pull Request #{pr_number} merged')
            logger.info(f'Added files: {added_files}')
            logger.info(f'Modified files: {modified_files}')
            logger.info(f'Removed files: {removed_files}')
            
            return jsonify({'status': 'success'}), 200

        return jsonify({'status': 'ignored'}), 200

if __name__ == '__main__':
    app.run(debug=True ,port=5052,  host='0.0.0.0')
