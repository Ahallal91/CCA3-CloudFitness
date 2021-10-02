# Cloud Computing - CloudFitness Application

**Team Members:**

* Alicia Hallal
* Thomas Haddad

# What is this project about?

Usage of fitness and health technology, platforms and applications are steadily on the rise, with 39% of adult Australians confirming that they used digital technology to assist in meeting their fitness goals during lockdowns[1]. As such, there is an increasing demand for applications which help users create, plan, and manage their exercises and workouts. Many existing web or mobile applications aim to do just that, but often either provide a broad array of services not useful to these specific needs or are too restrictive and lack any meaningful user interaction.
CloudFitness is a web application that is designed to help users quickly find exercises appropriate for their experience level and interests. Users can select from exercises contained within the public database or can create their own custom exercises if they do not already exist. The motivation for this application is to help users engage with particular exercises so that other like-minded users can benefit from the same exercises by the following: reading their comments, viewing the likes on the exercises, and building their exercise profile pages. This way they can build more efficient and enjoyable exercise routines with the exposure of different exercises and user comments.
CloudFitness is made up of three separate applications which all provide specific functionalities.

## Functionality of Main User Application
* Users can search exercises by their names
* Allow users to view exercise view and like counts
* Allow users to comment on exercises
* Users can add exercises to their profiles
* Users can submit their own exercises via upload functionality, these must be approved before being published, or upload personal exercises to their profile.

## Functionality of Admin Application

* Load exercises from API Gateway
* Edit exercises on API Gateway
* Set approved exercises to pending
* Set pending exercises to approved
* View all exercises available from API gateway

## REST API

* Get all exercises in the database
* Get exercises by type and name
* Get exercises by approved status
* Update exercise approved status (this requires an API key)

