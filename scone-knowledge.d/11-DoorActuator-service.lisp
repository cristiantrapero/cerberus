(in-context {dharma})

(new-action-type {actuate_bolt}
		 :agent-type {actuator}
		 :object-type {bolt})


(new-context {actuate_bolt bc} {dharma})
(new-is-a {actuate_bolt bc} {before context})
(x-is-the-y-of-z {actuate_bolt BC} {before context} {actuate_bolt})

(new-context {actuate_bolt ac} {actuate_bolt bc})
(new-is-a {actuate_bolt ac} {after context})
(x-is-the-y-of-z {actuate_bolt ac} {after context} {actuate_bolt})


(in-context {actuate_bolt BC})
(new-indv {authorizated to actuate bolt} {command execution by authorised person})


(in-context {dharma})
(new-indv {DoorActuator-service-instance} {DigitalSink})
(new-indv {DoorActuator.notify} {dharma-method})
(new-is-a {DoorActuator.notify} {DigitalSink.notify})

(x-is-a-y-of-z {DoorActuator.notify} {implemented-method} {DoorActuator-service-instance})

(new-statement {DoorActuator-service-instance}  {performs action through} {actuate_bolt} :c {DoorActuator.notify})

(new-statement {actuate_bolt} {causes} {open door})


(new-indv {door-actuator} {proxy})
(x-is-the-y-of-z {door-actuator} {service-proxy} {DoorActuator-service-instance})
