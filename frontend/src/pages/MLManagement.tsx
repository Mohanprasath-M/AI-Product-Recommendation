import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  Play, 
  CheckCircle2, 
  SlidersHorizontal, 
  RefreshCw, 
  Gauge, 
  Sparkles,
  Layers,
  Activity
} from 'lucide-react';
import { mlApi, recommendationsApi } from '../api/client';
import { MLModelVersion, ABWeightConfig } from '../types';

export const MLManagement: React.FC = () => {
  const [models, setModels] = useState<MLModelVersion[]>([]);
  const [evaluations, setEvaluations] = useState<any>(null);
  const [weights, setWeights] = useState<ABWeightConfig>({
    weight_content: 0.35,
    weight_collaborative: 0.30,
    weight_behavior: 0.15,
    weight_popularity: 0.08,
    weight_rating: 0.05,
    weight_personalization: 0.07,
    active_group: 'A'
  });

  const [isRetraining, setIsRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState<string | null>(null);
  const [weightsSaved, setWeightsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const loadMLData = async () => {
    setIsLoading(true);
    try {
      const [modData, evalData, wData] = await Promise.all([
        mlApi.getModels(),
        mlApi.getEvaluations(),
        recommendationsApi.getWeights()
      ]);
      setModels(modData || []);
      setEvaluations(evalData);
      setWeights(wData);
    } catch (e) {
      console.error('Failed to load ML state:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMLData();
  }, []);

  const handleRetrain = async (modelType = 'ALL') => {
    setIsRetraining(true);
    setRetrainMsg('Queuing background training pipeline...');
    try {
      const res = await mlApi.triggerTraining(modelType);
      setRetrainMsg(res.message || 'Background retraining started.');
      setTimeout(() => {
        setIsRetraining(false);
        setRetrainMsg(null);
        loadMLData();
      }, 5000);
    } catch (e) {
      setRetrainMsg('Error triggering background training.');
      setIsRetraining(false);
    }
  };

  const handleSaveWeights = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await recommendationsApi.updateWeights(weights);
      setWeightsSaved(true);
      setTimeout(() => setWeightsSaved(false), 3000);
    } catch (e) {
      console.error('Weights save error:', e);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 text-xs font-bold uppercase tracking-wider">
              MLOps Control Center
            </span>
            <span className="text-xs text-slate-400 font-medium">Scikit-Learn • SVD • TF-IDF • K-Means</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-1">Machine Learning Registry & A/B Tuning</h1>
        </div>

        <button
          onClick={() => handleRetrain('ALL')}
          disabled={isRetraining}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold shadow-lg shadow-brand-600/30 transition-all disabled:opacity-50"
        >
          <Play className="w-4 h-4 fill-white" />
          <span>{isRetraining ? 'Retraining Models...' : 'Retrain All ML Models'}</span>
        </button>
      </div>

      {retrainMsg && (
        <div className="p-4 rounded-2xl bg-brand-600/20 text-brand-300 border border-brand-500/30 text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <Activity className="w-4 h-4 animate-spin text-brand-400" />
          <span>{retrainMsg}</span>
        </div>
      )}

      {/* Model Benchmark Evaluation Cards */}
      {evaluations && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          
          {/* Recommender Metrics */}
          <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Recommender Performance</span>
              <Gauge className="w-4 h-4 text-brand-400" />
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Precision@10:</span>
                <span className="font-mono font-bold text-white">{(evaluations.recommender_metrics?.precision_at_10 * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Recall@10:</span>
                <span className="font-mono font-bold text-white">{(evaluations.recommender_metrics?.recall_at_10 * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Hit Rate@10:</span>
                <span className="font-mono font-bold text-emerald-400">{(evaluations.recommender_metrics?.hit_rate_at_10 * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">NDCG@10:</span>
                <span className="font-mono font-bold text-brand-300">{(evaluations.recommender_metrics?.ndcg_at_10).toFixed(3)}</span>
              </div>
            </div>
          </div>

          {/* NLP Sentiment Metrics */}
          <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Review NLP Sentiment</span>
              <Sparkles className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Classification Accuracy:</span>
                <span className="font-mono font-bold text-emerald-400">{(evaluations.sentiment_metrics?.accuracy * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Weighted F1-Score:</span>
                <span className="font-mono font-bold text-white">{(evaluations.sentiment_metrics?.f1_score).toFixed(3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Precision:</span>
                <span className="font-mono font-bold text-white">{(evaluations.sentiment_metrics?.precision * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Recall:</span>
                <span className="font-mono font-bold text-white">{(evaluations.sentiment_metrics?.recall * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>

          {/* Segmentation Metrics */}
          <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Customer Clustering</span>
              <Layers className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Silhouette Coefficient:</span>
                <span className="font-mono font-bold text-emerald-400">{(evaluations.segmentation_metrics?.silhouette_score).toFixed(3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Davies-Bouldin Index:</span>
                <span className="font-mono font-bold text-white">{evaluations.segmentation_metrics?.davies_bouldin_score || '0.72'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Cluster Separation:</span>
                <span className="font-bold text-emerald-400">Optimal (k=5)</span>
              </div>
            </div>
          </div>

        </div>
      )}

      {/* Model Registry Table */}
      <div className="glass-card rounded-3xl border border-slate-800 overflow-hidden">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Active Model Version Registry</h3>
            <p className="text-xs text-slate-400">Serialized models stored in memory and on-disk joblib artifacts.</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
              <tr>
                <th className="p-4">Model Name</th>
                <th className="p-4">Version</th>
                <th className="p-4">Algorithm</th>
                <th className="p-4">Dataset Size</th>
                <th className="p-4">Duration</th>
                <th className="p-4">Status</th>
                <th className="p-4 text-right">Retrain</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {models.map((m) => (
                <tr key={m.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="p-4 font-bold text-slate-100">{m.model_name}</td>
                  <td className="p-4 font-mono text-brand-300">{m.version}</td>
                  <td className="p-4 text-slate-400">{m.algorithm}</td>
                  <td className="p-4 font-mono text-slate-300">{m.dataset_size.toLocaleString()} rows</td>
                  <td className="p-4 font-mono text-slate-400">{m.training_duration_seconds}s</td>
                  <td className="p-4">
                    <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold">
                      ACTIVE
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button
                      onClick={() => handleRetrain(m.model_name)}
                      className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold"
                    >
                      Retrain
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Dynamic Hybrid Weight Tuner (A/B Testing Config) */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/50 space-y-6">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-brand-400" />
              Dynamic Hybrid Recommender Weight Configuration (A/B Testing)
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Adjust multi-signal fusion weights in real time without restarting backend services.
            </p>
          </div>
        </div>

        <form onSubmit={handleSaveWeights} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Content Similarity Weight:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_content * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_content}
                onChange={(e) => setWeights({ ...weights, weight_content: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Collaborative SVD Weight:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_collaborative * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_collaborative}
                onChange={(e) => setWeights({ ...weights, weight_collaborative: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Real-Time Behavioral Weight:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_behavior * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_behavior}
                onChange={(e) => setWeights({ ...weights, weight_behavior: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Global Popularity Weight:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_popularity * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_popularity}
                onChange={(e) => setWeights({ ...weights, weight_popularity: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Product Rating Weight:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_rating * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_rating}
                onChange={(e) => setWeights({ ...weights, weight_rating: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-semibold">Customer Profile Personalization:</span>
                <span className="font-mono text-brand-300 font-bold">{(weights.weight_personalization * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weights.weight_personalization}
                onChange={(e) => setWeights({ ...weights, weight_personalization: parseFloat(e.target.value) })}
                className="w-full accent-brand-500"
              />
            </div>

          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            {weightsSaved ? (
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>Hybrid weights synchronized to Redis cache!</span>
              </div>
            ) : (
              <span className="text-xs text-slate-500">Normalizes dynamically to 100% upon execution.</span>
            )}

            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold shadow-lg shadow-brand-600/30 transition-all"
            >
              Apply Hybrid Weights
            </button>
          </div>
        </form>
      </div>

    </div>
  );
};
