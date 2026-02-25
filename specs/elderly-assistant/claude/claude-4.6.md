Here's the rewritten prompt:

---

**Design a comprehensive AI Assistant app for elderly users from non-English-speaking backgrounds.**

---

**Context & Target Users**

The app targets elderly parents who find smartphones overwhelming due to language barriers, unfamiliar symbolism/cultural differences, and physical or cognitive challenges (e.g., trembling hands, memory decline, difficulty navigating UI). Despite this, they want to use apps like YouTube, Facebook, and WhatsApp to stay entertained and connected with family abroad or in other cities.

The assistant should be primarily voice-driven, always-on, and operable without navigating complex UI.

---

**Core Features to Design**

**1. Daily Routine Management**
- Voice reminders for: wake-up, yoga/exercise, medications (persistent/nagging until acknowledged), meals (lunch, snacks, dinner), and bedtime
- Calendar integration (Google Calendar) for appointments and important dates
- All reminders configurable by remote family members or in-app

**2. Health & Emergency Monitoring**
- Integrate with Apple HealthKit and Google Health Connect to read/write health data (e.g., blood pressure, heart rate, glucose)
- When a health metric exceeds a defined threshold: automatically contact emergency services, notify pre-nominated family contacts, and verbally reassure the user ("Help is on the way")
- Support a prioritised emergency contact list (spouse, children, etc.)

**3. Communication & Notifications**
- Read incoming messages and notifications aloud, filtered by importance
- Allow the user to send texts and make calls using voice commands
- Provide hands-free access to WhatsApp, Facebook, and similar apps via voice

**4. Entertainment & Scheduled Media**
- Play music (e.g., bhajans, devotional) at scheduled or on-demand times
- Play yoga/exercise videos at scheduled times
- Read news aloud at a predefined daily time
- Launch YouTube or other media via voice command

**5. Voice-Personalised Interaction**
- Train a lightweight voice/speech model on user-provided voice samples to recognise the individual's accent, speech patterns, and regional dialect
- Handle natural language queries in the user's native or mixed language (e.g., Hinglish, Cantonese-English)
- Explain how to use phone features when asked

---

**Remote Configuration (Critical)**
- Family members must be able to remotely configure the app via a companion interface (web or mobile)
- Configurable items: reminders and schedules, emergency contacts and thresholds, media playlists, notification filters, language and dialect settings
- Changes pushed to the device in real time

---

**Security**
- Primary authentication: voice recognition as biometric fingerprint
- Fallback: numeric PIN

---

**Runtime**
- The assistant runs 24/7 as a persistent background service
- Must handle interruptions (calls, notifications) gracefully and resume context

---

**Deliverables Expected from the LLM**

Provide a detailed breakdown of:
1. System architecture (frontend, backend, AI/ML components, health integrations)
2. Key components and tech stack recommendations for each feature area
3. Voice model design: training pipeline, dialect handling, on-device vs. cloud inference tradeoffs
4. Remote config architecture (how the companion app pushes config to the device)
5. Health API integration design and emergency response flow
6. Security model (voice biometrics + PIN fallback)
7. UX considerations specific to elderly users with cognitive or physical limitations

---