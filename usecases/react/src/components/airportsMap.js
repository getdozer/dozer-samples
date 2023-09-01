import GoogleMapReact from 'google-map-react';
import { useEffect, useState } from "react";
import { useDozerEndpointQuery } from "@dozerjs/dozer-react";

const Marker = ({ text }) => <div style={{
  color: "white",
  fontWeight: "bold",
  border: '6px solid #b0488c',
  textAlign: 'center',
  backgroundColor: '#b0488c',
  width: '80px',
  height: '20px',
}}>{text}</div>;

function AirportsMap() {
  const [airports, setAirports] = useState([]);
  const { records } = useDozerEndpointQuery('pickup', { query: { limit: 5000 }, watch: true })

  useEffect(() => {
    setAirports(records);
  }, [records])

  const defaultProps = {
    center: {
      lng: 50.993667602539063,
      lat: 50.7
    },
    zoom: 4
  };

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: "AIzaSyAV1g7kB_iY7H3BNjgtbc7Aaa8q1_isDJA" }}
        defaultCenter={defaultProps.center}
        defaultZoom={defaultProps.zoom}
      >
        {airports.map(airport =>
          <Marker key={airport.Zone}
            lat={Number(airport.latitude)}
            lng={Number(airport.longitude)}
            text={airport.Zone + ' (' + airport.trips + ')'} />
        )}
      </GoogleMapReact>
    </div>
  );
}

export default AirportsMap;