import GoogleMapReact from 'google-map-react';
import { useOnEvent, useQueryCommon } from "@getdozer/dozer-react";
import { useEffect, useState } from "react";
import { OperationType } from "@getdozer/dozer-js/lib/esm/generated/protos/types";

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
  const { records } = useQueryCommon('airports_count');

  useOnEvent('airports_count', (data, fields, primaryIndexKeys, mapper) => {
    if (fields.length) {
      setAirports(records => {
        if (data.getTyp() === OperationType.UPDATE) {
          let oldValue = mapper.mapRecord(data.getOld().getValuesList());
          let existingIndex = records.findIndex(v => v[primaryIndexKeys[0]] === oldValue[primaryIndexKeys[0]])

          if (records.length > 0) {
            if (existingIndex > -1) {
              records[existingIndex] = mapper.mapRecord(data.getNew().getValuesList());
              return [...records];
            } else {
              return [...records, mapper.mapRecord(data.getNew().getValuesList())];
            }
          }
        } else if (data.getTyp() === OperationType.INSERT) {
          return [...records, mapper.mapRecord(data.getNew().getValuesList())];
        }

        return records
      });
    }

  });

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