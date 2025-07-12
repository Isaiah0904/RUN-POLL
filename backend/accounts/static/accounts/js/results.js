
import { API_CONFIG } from './config.js';
import { Auth } from './auth.js';

class ResultsManager {
    async calculateResults(electionId) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/elections/${electionId}/results/calculate/`, {
                method: 'POST',
                headers: Auth.getAuthHeaders()
            });
            return await response.json();
        } catch (error) {
            console.error('Error calculating results:', error);
            return { success: false, error: 'Failed to calculate results' };
        }
    }

    async exportResults(electionId, format = 'pdf') {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/elections/${electionId}/results/export/?format=${format}`, {
                headers: Auth.getAuthHeaders()
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `election-results-${electionId}.${format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                return { success: true };
            } else {
                return { success: false, error: 'Export failed' };
            }
        } catch (error) {
            console.error('Error exporting results:', error);
            return { success: false, error: 'Export failed' };
        }
    }

    generateResultsChart(data, canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        // Simple bar chart implementation
        const maxVotes = Math.max(...data.map(d => d.votes));
        const barWidth = canvas.width / data.length;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        data.forEach((item, index) => {
            const barHeight = (item.votes / maxVotes) * (canvas.height - 50);
            const x = index * barWidth;
            const y = canvas.height - barHeight - 30;
            
            // Draw bar
            ctx.fillStyle = `hsl(${index * 360 / data.length}, 70%, 50%)`;
            ctx.fillRect(x + 10, y, barWidth - 20, barHeight);
            
            // Draw label
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(item.name, x + barWidth/2, canvas.height - 10);
            ctx.fillText(item.votes, x + barWidth/2, y - 5);
        });
    }
}

export { ResultsManager };
