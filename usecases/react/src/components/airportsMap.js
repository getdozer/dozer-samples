import GoogleMapReact from 'google-map-react';
import { useEffect, useState } from "react";
import { useDozerEndpointQuery } from "@dozerjs/dozer-react";

const Marker = ({ text }) => <div style={{
  color: "white",
  fontWeight: "bold",
  border: '6px solid #b0488c',
  textAlign: 'center',
  backgroundColor: '#b0488c',
  width: '75px',
  height: '15px',
}}>{text}</div>;

function AirportsMap() {
  const [airports, setAirports] = useState([]);
  const { records } = useDozerEndpointQuery('airports_count', { query: { limit: 5000 }, watch: true })

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
          <Marker key={airport.airport}
                  lat={airport.coordinates?.getY()}
                  lng={airport.coordinates?.getX()}
                  text={airport.airport + ' (' + airport.tickets + ')'}/>
        )}
      </GoogleMapReact>
    </div>
  );
}

export default AirportsMap;