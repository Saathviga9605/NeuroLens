import './PrivacyEnhancements.css';

const PrivacyPage = () => {
  const styles = {
    container: { maxWidth: 860, margin: '0 auto', padding: 28, fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial", color: 'var(--text, #eaf6f2)' },
    h1: { margin: 0, fontSize: 22, fontWeight: 800 },
    p: { marginTop: 12, color: 'var(--muted)' },
    list: { marginTop: 8, color: 'var(--muted)' }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.h1}>Privacy & Ethics</h2>

      <p style={styles.p}><strong>Local-first:</strong> All analysis runs locally by default. Your raw data stays on your device unless you explicitly export or share it.</p>

      <p style={styles.p}><strong>Non-diagnostic disclaimer:</strong> Outputs are informational and research-focused only, not medical or clinical advice. Consult a qualified professional for health concerns.</p>
    </div>
  );
};

export default PrivacyPage;

