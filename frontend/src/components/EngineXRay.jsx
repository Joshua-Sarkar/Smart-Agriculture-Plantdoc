import { useEffect, useState } from 'react'
import { Activity, BrainCircuit } from 'lucide-react'
import CNNVisualization from './CNNVisualization'
import IoTGauges from './IoTGauges'
import ConfidenceComparison from './ConfidenceComparison'

function EngineXRay({ results, isAnalyzing, iotData }) {
  return (
    <div className="flex flex-col h-full bg-[rgba(10,15,13,0.6)] backdrop-blur-md rounded-2xl border border-[var(--gold-dim)] overflow-hidden shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
      <div className="p-8 border-b border-[var(--gold-dim)] bg-gradient-to-r from-[rgba(212,175,55,0.05)] to-transparent">
        <h2 className="text-[var(--gold)] font-bold tracking-widest uppercase flex items-center gap-2">
          <Activity size={20} />
          Engine X-Ray
        </h2>
      </div>

      <div className="flex-1 p-10 flex flex-col justify-center relative overflow-y-auto custom-scrollbar">
        {!results ? (
          <div className="flex flex-col items-center justify-center text-center opacity-50">
            <BrainCircuit size={48} className="text-[var(--gold)] mb-4" />
            <p className="text-[var(--gold)] text-sm tracking-widest uppercase">Diagnostic Engine Idle</p>
          </div>
        ) : (
          <div className="flex flex-col gap-10">
            {/* CNN Layer Visualization */}
            <CNNVisualization isAnalyzing={isAnalyzing} />

            {/* Live IoT Sensor Gauges */}
            <div className="bg-[rgba(26,67,49,0.1)] border border-[var(--green-malachite)] p-6 rounded-xl">
              <IoTGauges 
                temperature={iotData?.temperature || 24}
                humidity={iotData?.humidity || 70}
                moisture={iotData?.moisture || 60}
                pulse={iotData?.pulse || false}
              />
            </div>

            {/* Confidence Comparison */}
            <div className="bg-[rgba(26,67,49,0.1)] border border-[var(--green-malachite)] p-6 rounded-xl">
              <ConfidenceComparison
                aiConfidence={results.top_prediction.confidence}
                weightedConfidence={results.weighted_confidence}
              />
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-[var(--gold-dim)] bg-[rgba(10,15,13,0.8)] text-center">
        <p className="text-[var(--gold-dim)] text-xs tracking-widest uppercase">
          Real-Time Diagnostics Active
        </p>
      </div>
    </div>
  )
}

export default EngineXRay
