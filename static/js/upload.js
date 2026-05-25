document.addEventListener("DOMContentLoaded", () => {
    const uploadContainer = document.getElementById('uploadContainer');
    const fileInput = document.getElementById('fileInput');
    const loadingSpinner = document.getElementById('uploadLoading');
    const uploadText = document.getElementById('uploadText');
    const uploadSubtext = document.getElementById('uploadSubtext');
    
    if(!uploadContainer) return;

    uploadContainer.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, () => uploadContainer.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, () => uploadContainer.classList.remove('dragover'), false);
    });

    uploadContainer.addEventListener('drop', (e) => {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];
        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        loadingSpinner.style.display = 'block';
        uploadText.innerText = 'Uploading...';
        uploadSubtext.style.display = 'none';

        fetch('/api/upload/file', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = 'none';
            if(data.error) {
                uploadText.innerText = 'Upload failed';
                uploadSubtext.innerText = data.error;
                uploadSubtext.style.display = 'block';
                uploadSubtext.style.color = '#bc4749';
            } else {
                uploadText.innerText = 'Upload successful!';
                uploadSubtext.innerText = `${data.row_count} rows loaded. Redirecting to cleaning...`;
                uploadSubtext.style.display = 'block';
                uploadSubtext.style.color = '#6a994e';
                
                // Set dataset_id in local storage or session
                localStorage.setItem('current_dataset_id', data.dataset_id);
                
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            }
        })
        .catch(() => {
            loadingSpinner.style.display = 'none';
            uploadText.innerText = 'Upload failed';
        });
    }
});
