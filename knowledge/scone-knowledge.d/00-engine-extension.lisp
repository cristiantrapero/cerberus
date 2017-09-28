
;; Extending ERIS
;; I had this code, I believe it's Scott's 
(new-type {expandable event} {event})
(new-type {ordered event} {event})

(new-complete-split-subtypes {expandable event}
 '({sequential event}
   {all event}
   {or event}
   {iterative event}
   {concurrent event}
   {optional event}
   {conditional event}))

;; 1. Sequantial Events

;; sequential event's subevent have two relations defined for them
;; they can be viewed as a chain of events weaved with these relations
;(get-the-x-role-of-y {subevent} {sequential event} :iname {ordered event})

;; both these relations belong to a sequential event when used as statements.
;; These sequential events may use the same event twice, to keep the ordering
;; right we need indeces for each relation. That is the c-value
(new-relation {happens before} :a-inst-of {ordered event}
			       :b-inst-of {ordered event}
			       :c-inst-of {integer}
			       :english '(:relation
					  :inverse-relation "happens after")
			       :transitive t)
(new-relation {happens after}  :a-inst-of {ordered event}
			       :b-inst-of {ordered event}
			       :english '(:relation
					  :inverse-relation "happens before")
			       :transitive t)


;; we might have cycles, so keep a head of the sequence so that we know where to start
(new-indv-role {first ordered event} {sequential event} {ordered event})
(new-indv-role {last ordered event} {sequential event} {ordered event})

;; 2. ALL Events
(new-indv-role {comprising event} {all event} {event})
;; 3. OR Events
;; 4. Optional Events
;; 5. Concurrent Events
;; Being a subevent of these is sufficient knowledge to reason about them.


;; 6. Iterative Events

;; there are two types, these are complete and split, for now
(new-complete-split-subtypes {iterative event}
 '({do n times event} {do until event}))

;;do n times events have a number of iterations
(new-indv-role {number of iterations} {do n times event} {integer})

;;do until events have a termination clause function
(new-indv-role {termination clause} {do until event} {function})


;; 7. Conditional Events

;; Conditional events have predicates.
(new-indv-role {predicate} {conditional event} {function})


;; Functions for dealing with contexts
(defun get-before-context-of (act1)
  (let ((bc-elem (lookup-element (the-x-role-of-y {before context} act1)))) 
    (if (incoming-a-wires bc-elem)
	(b-wire (lookup-element (car (incoming-a-wires bc-elem)))))))

(defun get-after-context-of (act1)
  (let ((bc-elem (lookup-element (the-x-role-of-y {after context} act1))))  
    (if (incoming-a-wires bc-elem)
	(b-wire (lookup-element (car (incoming-a-wires bc-elem)))))))

(defun in-after-context-of (act1)
  (if (get-after-context-of act1)
      (in-context (get-after-context-of act1))
      *context*))

(defun in-before-context-of (act1)
  (if (get-before-context-of act1)
      (in-context (get-before-context-of act1))
      *context*))

(defun list-context-contents (cxt)
  "List all the elements define in context. Elements are mainly
relations, and those which are not, such as actions or events, are
turned into relations using the generic relation --causes--"
  (let ((temp-list '()))
    (dolist (rel (incoming-context-elements (lookup-element cxt)))
      (let* ((a (a-wire (lookup-element rel)))
	     (b (b-wire (lookup-element rel))))
	(if (not (eq (is-x-a-y? rel {event}) ':YES))
	    (push (list a rel b) temp-list))))
    temp-list))

;; Function for finding causes of an event
(defun list-causes (evt)
 "List all the actions and events that have been described as the
  cause of a given event evt. The realtion {causes} is used to find
  these actions and events"
  (with-markers (m1)
    (progn
      (mark-rel-inverse  {causes} evt m1)
      (car (list-most-specific m1)))))

(defun list-effects-of (action)
 "List all the events caused by  a given action. The realtion {causes}
  is used to find these actions and events"
  (with-markers (m1)
    (progn
      (mark-rel  {causes} action m1)
      (car (list-most-specific m1)))))


(defun get-the-method-that-performs-action (action)
  "Returns the methods that perform a given ACTION"
  (let ((service-list (list-rel-inverse {performs action through} action))
	(method-list (list-children (lookup-element (c-element  {performs action through})))))
    (dolist (service service-list)
      (dolist (method method-list)
	(when
	    (eq (lookup-element service) (lookup-element (the-x-inverse-of-y {implemented-method} method)))
	  (return-from  get-the-method-that-performs-action (lookup-element method)))))))
	  
      
(defun get-the-method-that-causes-event (event)
  "Returns the method that causes a given event"
  (let ((method-list (list-children (c-element {causes event through})))
	(service (car (list-rel-inverse {causes event through} event))))
    (dolist (method method-list)
      (when
	  (eq (lookup-element (a-element (car (incoming-c-elements method))))
	      (lookup-element service))
	(return-from  get-the-method-that-causes-event (lookup-element method))))))

(defun get-the-service-proxy-for-action (action)
  "Returns the  proxy that  caters for  that action.  If there  is not
service for  that, it looks  for the event  caused by that  action and
trace back the service that causes it."
  (if (get-the-service-proxy-that-performs-an-action action)
      (return-from  get-the-service-proxy-for-action (get-the-service-proxy-that-performs-an-action action)))
  (let ((event (list-effects-of action)))
    (return-from get-the-service-proxy-for-action (get-the-service-proxy-that-causes-an-event event))))

(defun get-the-required-argument-for-action (action)
  "Returns the required argument for the methods that performs or causes and ACTION."
  (if (not (get-the-method-that-performs-action action))
      (return-from get-the-required-argument-for-action  nil))
  (let ((method (get-the-method-that-performs-action action)))
    (list-all-x-of-y {required-argument} method)))

(defun get-the-service-proxy-that-returns-an-argument (argument)
  "Returns the service proxy for a method capable of returning a saught argument."
  (let ((service-proxies-list '())
	(methods-list (list-all-x-inverse-of-y  {returned-value} argument)))
    (dolist (method methods-list)
      (let ((service (the-x-inverse-of-y {implemented-method} method)))
	(push (the-x-of-y {service-proxy} service) service-proxies-list)))
    service-proxies-list))
	
(defun get-the-service-proxy-that-performs-an-action (action)
  "Returns the proxy of the service whose method performs an ACTION"
  (if (not (get-the-method-that-performs-action action))
      (return-from get-the-service-proxy-that-performs-an-action nil))
  (let* ((method (get-the-method-that-performs-action action))
	(service (the-x-inverse-of-y {implemented-method} method)))
    (the-x-of-y {service-proxy} service)))
    
(defun get-the-service-proxy-that-causes-an-event (event)
  "Returns the proxy of the service whose method causes an EVENT"
  (let* ((service (get-the-service-that-causes-an-event event)))
    (the-x-of-y {service-proxy} service)))

(defun get-the-service-that-causes-an-event (event)
  "Returns the service that casues a given event"
  (car (list-rel-inverse {causes event through} event)))


(defun get-the-events-required-for-action (action)
  "Returns the events that are pre-requirements for ACTION to take place"
  (let ((required-events-list '())
	(content-list (list-context-contents (get-before-context-of action))))
    (dolist (content content-list)
      (when
	  (and (not (null (caddr content)))
	  (eq (is-x-a-y? (caddr content) {event})
	      :YES))
	(push (parent-element (caddr content)) required-events-list)))
    required-events-list))
	
  
(defun simple-is-x-a-y-of-z? (x y z)
  (setq x (lookup-element-test x))
  (setq y (lookup-element-test y))
  (setq z (lookup-element-test z))
  (with-markers (m1)
    (progn
      (mark-all-x-of-y y z m1)
      (marker-on? x m1))))

(defun is-x-a-y-of-z? (x y z)
  (setq x (lookup-element-test x))
  (setq y (lookup-element-test y))
  (setq z (lookup-element-test z))
  (let ((err nil))
    (cond ((simple-is-x-a-y-of-z? x y z) :yes)
	  ((setq err (incompatible? x y))
	   (values :no err))
	  (t :maybe))))
