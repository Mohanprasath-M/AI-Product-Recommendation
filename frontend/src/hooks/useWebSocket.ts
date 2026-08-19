import { useEffect, useRef, useState, useCallback } from 'react';
import { LiveActivityItem } from '../types';

export const useWebSocket = (userId?: string) => {
  const [liveEvents, setLiveEvents] = useState<LiveActivityItem[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws?client_id=${userId || 'guest'}`;

    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (evt) => {
        try {
          const msg = JSON.parse(evt.data);
          if (msg.type === 'LIVE_EVENT' && msg.data) {
            setLiveEvents((prev) => [msg.data, ...prev.slice(0, 49)]);
          }
        } catch {
          // Non-json ping/pong
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        // Reconnect after 3s
        setTimeout(connect, 3000);
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch {
      setIsConnected(false);
    }
  }, [userId]);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  return { liveEvents, isConnected };
};
