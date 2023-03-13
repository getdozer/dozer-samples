import AirportsMap from "./airportsMap";
import DeparturesCount from "./departuresCount";

export const AirportsWrapper = () => {
  return <div style={{ height: '100vh', width: '100%', display: 'flex', flexDirection: 'row' }}>
    <AirportsMap />
    <DeparturesCount />
  </div>
}