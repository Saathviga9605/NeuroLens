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
      <h2 style={styles.h1}>Privacy & Ethics — Quick Notes</h2>

      <p style={styles.p}><strong>Local-first:</strong> All analysis runs locally by default. Your raw data stays on your device unless you explicitly export or share it.</p>

      <p style={styles.p}><strong>User controls:</strong> You can export or delete any stored results at any time. No telemetry or external uploads occur without your explicit consent.</p>

      <p style={styles.p}><strong>Non-diagnostic disclaimer:</strong> Outputs are informational and research-focused only — not medical or clinical advice. Consult a qualified professional for health concerns.</p>

      <div style={styles.list}>
        <ul>
          <li>Export: user-initiated only</li>
          <li>Delete: immediate local removal</li>
          <li>Opt-in cloud features (if added) will require explicit consent</li>
        </ul>
      </div>

      <p style={{ ...styles.p, marginTop: 20 }}>For any privacy questions or to request deletion instructions, see the project README or contact the application owner.</p>
    </div>
  );
};

export default PrivacyPage;
