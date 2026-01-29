document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    const scorePath = document.getElementById('scorePath');
    const scoreValue = document.getElementById('scoreValue');
    const missingSkillsList = document.getElementById('missingSkills');
    const improvementTipsList = document.getElementById('improvementTips');
    const loader = analyzeBtn.querySelector('.loader');
    const btnText = analyzeBtn.querySelector('.btn-text');

    const resumeInput = document.getElementById('resumeFile');
    const dropZone = document.getElementById('dropZone');
    const fileNameDisplay = document.getElementById('fileName');
    const jdInput = document.getElementById('jdInput');

    // Handle File Selection
    dropZone.addEventListener('click', () => resumeInput.click());

    resumeInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            updateFileName(e.target.files[0].name);
        }
    });

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            resumeInput.files = e.dataTransfer.files;
            updateFileName(e.dataTransfer.files[0].name);
        }
    });

    function updateFileName(name) {
        fileNameDisplay.textContent = name;
        fileNameDisplay.classList.add('selected');
    }

    analyzeBtn.addEventListener('click', async () => {
        const resumeFile = resumeInput.files[0];
        const jdText = jdInput.value.trim();

        if (!resumeFile || !jdText) {
            alert('Please provide both a resume PDF and a job description.');
            return;
        }

        // Show loading state
        loader.classList.remove('hidden');
        btnText.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('resume_file', resumeFile);
        formData.append('job_description', jdText);

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to analyze resume');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis. Please ensure the backend is running.');
        } finally {
            loader.classList.add('hidden');
            btnText.textContent = 'Analyze Match';
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsSection.classList.remove('hidden');

        // Update Score
        const score = data.match_score;
        scoreValue.textContent = `${Math.round(score)}%`;
        scorePath.style.strokeDasharray = `${score}, 100`;

        // Update Skills
        missingSkillsList.innerHTML = '';
        if (data.missing_skills.length > 0) {
            data.missing_skills.forEach(skill => {
                const li = document.createElement('li');
                li.textContent = skill;
                missingSkillsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No critical missing skills identified!';
            li.style.borderLeftColor = '#10b981';
            missingSkillsList.appendChild(li);
        }

        // Update Tips
        improvementTipsList.innerHTML = '';
        data.improvement_tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            improvementTipsList.appendChild(li);
        });

        // Smooth Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});
