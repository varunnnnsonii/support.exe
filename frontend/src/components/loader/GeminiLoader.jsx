import React from 'react';

const GeminiLoader = () => {
  return (
    <div className="flex flex-col gap-2">
      <div className="h-5 w-10/12 origin-left animate-loading rounded-sm bg-gradient-to-r from-blue-50 from-30% via-blue-500/60 to-blue-50 to-70% bg-[length:200%] opacity-0" />
      <div className="h-5 w-full origin-left animate-loading rounded-sm bg-gradient-to-r from-blue-50 from-40% via-blue-500/60 to-blue-50 to-70% bg-[length:200%] opacity-0" />
      <div className="h-5 w-3/5 origin-left animate-loading rounded-sm bg-gradient-to-r from-blue-50 from-50% via-blue-500/60 to-blue-50 to-70% bg-[length:200%] opacity-0" />
    </div>
  );
};
export default GeminiLoader;