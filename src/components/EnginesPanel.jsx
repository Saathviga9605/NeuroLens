import React, { useState } from 'react';
import mockApi from '../services/mockApi';

const EngineTile = ({ name, status, onRun }) => {
  const color = status === 'Running' ? '#f59e0b' : status === 'Completed' ? 'var(--accent)' : status === 'Pending' ? '#9fb0d4' : '#6b7280';
  return (
    <div style={{ padding: 12, borderRadius: 8, background: 'rgba(255,255,255,0.02)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ fontWeight: 700 }}>{name}</div>
        <div style={{ fontSize: 12, color: '#bcd7e6' }}>{status}</div>
      </div>
      <div>
        <button onClick={onRun} style={{ padding: '6px 10px', background: color, border: 'none', color: '#fff', borderRadius: 6 }}>Run</button>
      </div>
    </div>
  );
};

const EnginesPanel = ({ onPartResult, onFusion, onNavigate }) => {
  const [statuses, setStatuses] = useState({ Behavioral: 'Idle', NLP: 'Idle', Voice: 'Idle', Fusion: 'Idle' });
  const [parts, setParts] = useState([]);
  const [error, setError] = useState(null);

  const runBehavior = async () => {
    try {
      setError(null);
      setStatuses(s => ({ ...s, Behavioral: 'Running' }));
      const res = await mockApi.behaviorAnalyze({ csv: '' });
      setParts(p => [...p, res]);
      setStatuses(s => ({ ...s, Behavioral: 'Completed' }));
      onPartResult && onPartResult(res);
      onNavigate && onNavigate('dashboard');
    } catch (err) {
      console.error('Behavior engine error', err);
      setStatuses(s => ({ ...s, Behavioral: 'Failed' }));
      setError('Behavior engine failed — check console for details');
    }
  };

  const runNLP = async () => {
    try {
      setError(null);
      setStatuses(s => ({ ...s, NLP: 'Running' }));
      const res = await mockApi.nlpAnalyze({ text: 'Simulation text input' });
      setParts(p => [...p, res]);
      setStatuses(s => ({ ...s, NLP: 'Completed' }));
      onPartResult && onPartResult(res);
      onNavigate && onNavigate('dashboard');
    } catch (err) {
      console.error('NLP engine error', err);
      setStatuses(s => ({ ...s, NLP: 'Failed' }));
      setError('NLP engine failed — check console for details');
    }
  };

  const runVoice = async () => {
    try {
      setError(null);
      setStatuses(s => ({ ...s, Voice: 'Running' }));
      const res = await mockApi.voiceAnalyze({ audioBlob: null });
      setParts(p => [...p, res]);
      setStatuses(s => ({ ...s, Voice: 'Completed' }));
      onPartResult && onPartResult(res);
      onNavigate && onNavigate('dashboard');
    } catch (err) {
      console.error('Voice engine error', err);
      setStatuses(s => ({ ...s, Voice: 'Failed' }));
      setError('Voice engine failed — check console for details');
    }
  };

  const runFusion = async () => {
    try {
      setStatuses(s => ({ ...s, Fusion: 'Running' }));
      const res = await mockApi.fusionScore({ parts });
      setStatuses(s => ({ ...s, Fusion: 'Completed' }));
      onFusion && onFusion(res);
      onNavigate && onNavigate('dashboard');
    } catch (err) {
      console.error('Fusion engine error', err);
      setStatuses(s => ({ ...s, Fusion: 'Failed' }));
    }
  };

  const runAll = async () => {
    setParts([]);
    await runBehavior();
    await runNLP();
    await runVoice();
    await runFusion();
  };

  return (
    <div className="glass" style={{ padding: 12, marginTop: 12 }}>
      {error && <div style={{ color: '#ffb4b4', marginBottom: 8 }}>{error}</div>}
      <div style={{ display: 'flex', gap: 12, alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontWeight: 800 }}>Cognitive Engines</div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={runAll} style={{ padding: '6px 10px', borderRadius: 6 }} disabled={Object.values(statuses).some(s => s === 'Running')}>Run All</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 12, marginTop: 12 }}>
        <EngineTile name="Behavioral" status={statuses.Behavioral} onRun={runBehavior} />
        <EngineTile name="NLP" status={statuses.NLP} onRun={runNLP} />
        <EngineTile name="Voice" status={statuses.Voice} onRun={runVoice} />
        <EngineTile name="Fusion" status={statuses.Fusion} onRun={runFusion} />
      </div>
    </div>
  );
};

export default EnginesPanel;
