const history = [];

document.getElementById('ask').addEventListener('click', async () => {
  const q = document.getElementById('question').value;
  const class_no = parseInt(document.getElementById('class-select').value, 10);
  if (!q) return;
  const chat = document.getElementById('chat');
  const userEl = document.createElement('div'); userEl.className = 'message user'; userEl.textContent = q; chat.appendChild(userEl);
  document.getElementById('question').value = '';

  console.log('Sending request:', { question: q, class_no, history });
  
  const res = await fetch('/api/chat/', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: q, class_no, history })
  });
  
  console.log('Response status:', res.status);
  
  let data;
  const botEl = document.createElement('div'); 
  botEl.className = 'message bot';
  
  if (!res.ok) {
    const errorText = await res.text();
    console.error('Error response:', errorText);
    botEl.textContent = `Error ${res.status}: ${errorText}`;
    botEl.style.color = 'red';
    chat.appendChild(botEl);
    return;
  }
  
  try {
    data = await res.json();
    console.log('Received data:', data);
    botEl.textContent = data.answer || JSON.stringify(data);
    chat.appendChild(botEl);
    history.push({ role: "user", content: q });
    history.push({ role: "assistant", content: data.answer });
  } catch (e) {
    console.error('Parse error:', e);
    botEl.textContent = `Failed to parse response: ${e.message}`;
    botEl.style.color = 'red';
    chat.appendChild(botEl);
  }
});