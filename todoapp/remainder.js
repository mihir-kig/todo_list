<script>
  // Step 1: Define task reminders from Django
  const tasks = [
    {% for i in todos %}
      {% if i.reminder_time %}
        {
          name: "{{ i.todo_name|escapejs }}",
          time: new Date("{{ i.reminder_time|date:'Y-m-d\\TH:i:s' }}")
        },
      {% endif %}
    {% endfor %}
  ];

  // Step 2: Ask for notification permission once page loads
  document.addEventListener("DOMContentLoaded", function () {
    if ("Notification" in window && Notification.permission !== "granted") {
      Notification.requestPermission().then(permission => {
        console.log("🔔 Notification permission:", permission);
      });
    }
  });

  // Step 3: Reminder check every 30 seconds
  function checkReminders() {
    const now = new Date();
    tasks.forEach(task => {
      const diff = task.time - now;
      if (diff > 0 && diff < 60000) {
        // Browser notification if allowed
        if ("Notification" in window && Notification.permission === "granted") {
          new Notification("⏰ Reminder", {
            body: task.name,
            icon: "{% static 'your_app/bell.png' %}" // optional icon
          });
        } else {
          alert("⏰ Reminder: " + task.name); // fallback if permission not granted
        }

        // Optional sound
        const audio = document.getElementById("alarmSound");
        if (audio) audio.play();
      }
    });
  }

  setInterval(checkReminders, 30000); // check every 30 sec
</script>
