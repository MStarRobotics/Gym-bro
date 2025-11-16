import { useEffect, useState } from 'react';

interface GeolocationState {
  loading: boolean;
  error: GeolocationPositionError | null;
  data: GeolocationCoordinates | null;
}

const useGeolocation = (): GeolocationState => {
  const [state, setState] = useState<GeolocationState>({
    loading: true,
    error: null,
    data: null,
  });

  useEffect((): void => {
    const onEvent = ({ coords }: GeolocationPosition): void => {
      setState({
        loading: false,
        error: null,
        data: coords,
      });
    };

    const onEventError = (error: GeolocationPositionError): void => {
      setState({
        loading: false,
        error,
        data: null,
      });
    };

    navigator.geolocation.getCurrentPosition(onEvent, onEventError, {
      enableHighAccuracy: true,
    });
  }, []);

  return state;
};

export default useGeolocation;
