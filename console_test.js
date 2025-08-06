// Test script to inject into browser console
// Copy and paste this into the browser console when on localhost:5173

console.log('🧪 Starting API test...');

async function testServerAPI() {
    try {
        console.log('📡 Making fetch request to http://127.0.0.1:5000/api/servers');
        const response = await fetch('http://127.0.0.1:5000/api/servers', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('📡 Response status:', response.status);
        console.log('📡 Response headers:', [...response.headers.entries()]);
        
        const data = await response.json();
        console.log('✅ Data received:', data);
        
        if (data.servers && Array.isArray(data.servers)) {
            console.log(`✅ Found ${data.servers.length} servers`);
            data.servers.forEach((server, index) => {
                console.log(`Server ${index + 1}:`, server);
            });
        } else {
            console.warn('⚠️ No servers array found in response');
        }
        
        return data;
    } catch (error) {
        console.error('❌ Fetch error:', error);
        return null;
    }
}

// Run the test
testServerAPI().then(result => {
    console.log('🏁 Test completed, result:', result);
});

// Also test if React state management is working
console.log('🔍 Checking if React is available:', typeof React !== 'undefined' ? 'Yes' : 'No');
console.log('🔍 Current URL:', window.location.href);
console.log('🔍 Origin:', window.location.origin);
