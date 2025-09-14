import { useRef, useEffect } from 'react';

export default function useScrollReveal({
  animationClass = 'animate-fade-in-up',
  threshold = 0.15,
} = {}) {
  const ref = useRef(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const handleIntersect = (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          node.classList.add(animationClass);
          node.classList.remove('opacity-0');
        }
      });
    };
    const observer = new window.IntersectionObserver(handleIntersect, { threshold });
    observer.observe(node);
    return () => observer.disconnect();
  }, [animationClass, threshold]);

  return ref;
} 