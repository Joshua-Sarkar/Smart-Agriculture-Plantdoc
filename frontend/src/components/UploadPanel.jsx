import React, { useRef } from 'react'

export default function UploadPanel({ image, loading, onUpload }) {
  const fileInputRef = useRef(null)

  const handleClick = () => {
    if (!loading) fileInputRef.current.click()
  }

  return (
    <div className="glass-panel rounded-lg p-6 relative flex items-center justify-center h-full w-full">
      <input 
        type="file"
        ref={fileInputRef}
        onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
        className="hidden"
        accept="image/*"
      />
      <button 
        onClick={handleClick}
        className={`px-8 py-4 bg-primary-container border border-sovereign-gold text-sovereign-gold font-label-caps text-label-caps uppercase tracking-widest hover:border-moss-green hover:text-moss-green transition-colors ${loading ? 'pulse-glow opacity-50 cursor-not-allowed' : ''}`}
      >
        {loading ? 'Initializing...' : 'Initialize Scan'}
      </button>
    </div>
  )
}
