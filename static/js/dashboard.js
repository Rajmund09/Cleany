document.addEventListener("DOMContentLoaded", () => {
    const datasetId = localStorage.getItem('current_dataset_id');
    
    if(!datasetId) {
        // If no dataset selected, guide user to upload
        document.getElementById('dashboardContent').innerHTML = `
            <div class="card slide-up">
                <p>No active dataset selected. Please <a href="/upload">upload a dataset</a> to get started.</p>
            </div>
        `;
        return;
    }
    
    // Load dataset summary
    fetch(`/api/analytics/summary/${datasetId}?use_cleaned=false`)
        .then(res => res.json())
        .then(data => {
            if(data.error) {
                console.error(data.error);
                return;
            }
            renderSummary(data);
        });
        
    function renderSummary(data) {
        document.getElementById('metricRows').innerText = data.summary.total_rows;
        document.getElementById('metricCols').innerText = data.summary.total_columns;
        document.getElementById('metricMissing').innerText = data.summary.total_missing;
        document.getElementById('metricScore').innerText = data.quality_score + '/100';
    }
    
    const btnClean = document.getElementById('btnClean');
    if(btnClean) {
        btnClean.addEventListener('click', () => {
            btnClean.innerText = 'Cleaning...';
            btnClean.disabled = true;
            
            const laborModal = document.getElementById('laborModal');
            const laborTitle = document.getElementById('laborTitle');
            if (laborModal) laborModal.style.display = 'flex';
            
            const steps = [
                "Scanning for duplicate records...",
                "Standardizing text & date formats...",
                "Imputing missing values...",
                "Identifying statistical outliers...",
                "Finalizing pristine dataset..."
            ];
            
            let stepIndex = 0;
            const interval = setInterval(() => {
                if(stepIndex < steps.length) {
                    laborTitle.innerText = steps[stepIndex];
                    stepIndex++;
                }
            }, 800);
            
            fetch(`/api/analytics/clean/${datasetId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    remove_duplicates: true,
                    format_columns: true,
                    missing_values: 'auto',
                    handle_outliers: 'clip'
                })
            })
            .then(res => res.json())
            .then(data => {
                const minWaitTime = (steps.length * 800);
                const timeElapsed = stepIndex * 800;
                const remainingTime = Math.max(0, minWaitTime - timeElapsed);
                
                setTimeout(() => {
                    clearInterval(interval);
                    laborTitle.innerText = "Cleaning Complete!";
                    document.querySelector('.labor-spinner').style.display = 'none';
                    
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                }, remainingTime);
            });
        });
    }
});
