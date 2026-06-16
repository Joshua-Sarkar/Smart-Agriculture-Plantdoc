import React from 'react'

export default function IoTGauges({ temperature, humidity, moisture, pulse }) {
  return (
    <div className="glass-panel rounded-lg p-6 relative">
      <div className="font-label-caps text-label-caps text-sovereign-gold mb-4 uppercase">Environmental Metrics</div>
      <div className="h-2 w-full bg-sovereign-gold/20 rounded-full overflow-hidden mt-8">
        <div 
          className="h-full bg-moss-green shadow-[0_0_10px_#4A6741] transition-all duration-1000"
          style={{ width: `${humidity}%` }}
        ></div>
      </div>
      <div className="flex justify-between mt-2 font-technical-data text-technical-data text-on-surface-variant/80">
        <span>Temp: {temperature}°</span>
        <span>Humid: {humidity}%</span>
        <span>Moist: {moisture}%</span>
      </div>
    </div>
  )
}
