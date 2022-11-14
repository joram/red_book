import './App.css';
import {Card, Icon, Image} from "semantic-ui-react";
import services from './services.json'


function Service(props){
  let keywords = props.keywords.join(" ")
  return <Card>
    <Image src={props.image} wrapped ui={false} />
    <Card.Content>
      <Card.Header>{props.name}</Card.Header>
      <Card.Meta>
        <span>keywords: {keywords}</span>
        <span>address: {props.address}</span>
        <span>telephone: {props.telephone}</span>
        <span>email: {props.email}</span>
        <span>openingHours: {props.openingHours}</span>
      </Card.Meta>
      <Card.Description>
        {props.description}
      </Card.Description>
    </Card.Content>
    <Card.Content extra>
      <a href={props.url}>{props.url}</a>
    </Card.Content>
  </Card>
}
function Services() {
  let serviceCards = services.map((service) => {
    console.log(service)
    let address = service.address
    if (typeof(address) === "object") {
      address = JSON.stringify(address)
    }
      return <Service
          name={service.name}
          image={service.thumbnail}
          description={service.description}
          keywords={service.keywords}
          url={service.url}
          email={service.email}
          telephone={service.telephone}
          openingHours={service.openingHours}
          address={address}
      />
  })
  return serviceCards
}

function App() {
  return (
    <div className="App">
      <Card.Group>
        <Services/>
      </Card.Group>
    </div>
  );
}

export default App;
