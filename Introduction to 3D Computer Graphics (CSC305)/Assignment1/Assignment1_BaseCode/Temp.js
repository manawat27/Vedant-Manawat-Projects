/*
    Name: Vedant Manawat
    VNumber: V00904582
    Date: Feb 16, 2021

    CSC 305 Assignment 1
*/

/*
    IMPORTANT NOTE:

    The majority of the code has been picked up from the base code we were provided with to get us started.
    All of my implementations are either functions I created or can be found in the render() function. 

    Functions created by me:
     1. drawGroundBox()
     2. drawRocks()
     3. firstSeaWeeds()
     4. fishMovement()
     5. drawDiver()
     6. allSeaWeeds()
*/

var canvas;
var gl;

var program ;

var near = 1;
var far = 100;


var left = -6.0;
var right = 6.0;
var ytop =6.0;
var bottom = -6.0;


var lightPosition2 = vec4(100.0, 100.0, 100.0, 1.0 );
var lightPosition = vec4(0.0, 0.0, 100.0, 1.0 );

var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0 );
var lightDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var lightSpecular = vec4( 1.0, 1.0, 1.0, 1.0 );

var materialAmbient = vec4( 1.0, 0.0, 1.0, 1.0 );
var materialDiffuse = vec4( 1.0, 0.8, 0.0, 1.0 );
var materialSpecular = vec4( 0.4, 0.4, 0.4, 1.0 );
var materialShininess = 30.0;

var ambientColor, diffuseColor, specularColor;

var modelMatrix, viewMatrix, modelViewMatrix, projectionMatrix, normalMatrix;
var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc;
var eye;
var at = vec3(0.0, 0.0, 0.0);
var up = vec3(0.0, 1.0, 0.0);

var RX = 0 ;
var RY = 0 ;
var RZ = 0 ;

var MS = [] ; // The modeling matrix stack
var TIME = 0.0 ; // Realtime
var prevTime = 0.0 ;
var resetTimerFlag = true ;
var animFlag = false ;
var controller ;

function setColor(c)
{
    ambientProduct = mult(lightAmbient, c);
    diffuseProduct = mult(lightDiffuse, c);
    specularProduct = mult(lightSpecular, materialSpecular);
    
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "specularProduct"),flatten(specularProduct) );
    gl.uniform4fv( gl.getUniformLocation(program,
                                         "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
                                        "shininess"),materialShininess );
}

window.onload = function init() {

    canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.5, 0.5, 1.0, 1.0 );
    
    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );
    

    setColor(materialDiffuse) ;

    Cube.init(program);
    Cylinder.init(9,program);
    Cone.init(9,program) ;
    Sphere.init(36,program) ;

    
    modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix" );
    normalMatrixLoc = gl.getUniformLocation( program, "normalMatrix" );
    projectionMatrixLoc = gl.getUniformLocation( program, "projectionMatrix" );
    
    
    gl.uniform4fv( gl.getUniformLocation(program, 
       "ambientProduct"),flatten(ambientProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "diffuseProduct"),flatten(diffuseProduct) );
    gl.uniform4fv( gl.getUniformLocation(program, 
       "specularProduct"),flatten(specularProduct) );	
    gl.uniform4fv( gl.getUniformLocation(program, 
       "lightPosition"),flatten(lightPosition) );
    gl.uniform1f( gl.getUniformLocation(program, 
       "shininess"),materialShininess );

	
	document.getElementById("sliderXi").oninput = function() {
		RX = this.value ;
		window.requestAnimFrame(render);
	}
		
    
    document.getElementById("sliderYi").oninput = function() {
        RY = this.value;
        window.requestAnimFrame(render);
    };
    document.getElementById("sliderZi").oninput = function() {
        RZ =  this.value;
        window.requestAnimFrame(render);
    };

    document.getElementById("animToggleButton").onclick = function() {
        if( animFlag ) {
            animFlag = false;
        }
        else {
            animFlag = true  ;
            resetTimerFlag = true ;
            window.requestAnimFrame(render);
        }
        console.log(animFlag) ;
		
		controller = new CameraController(canvas);
		controller.onchange = function(xRot,yRot) {
			RX = xRot ;
			RY = yRot ;
			window.requestAnimFrame(render); };
    };

    render();
}

// Sets the modelview and normal matrix in the shaders
function setMV() {
    modelViewMatrix = mult(viewMatrix,modelMatrix) ;
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix) );
    normalMatrix = inverseTranspose(modelViewMatrix) ;
    gl.uniformMatrix4fv(normalMatrixLoc, false, flatten(normalMatrix) );
}

// Sets the projection, modelview and normal matrix in the shaders
function setAllMatrices() {
    gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix) );
    setMV() ;
    
}

// Draws a 2x2x2 cube center at the origin
// Sets the modelview matrix and the normal matrix of the global program
function drawCube() {
    setMV() ;
    Cube.draw() ;
}

// Draws a sphere centered at the origin of radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
function drawSphere() {
    setMV() ;
    Sphere.draw() ;
}
// Draws a cylinder along z of height 1 centered at the origin
// and radius 0.5.
// Sets the modelview matrix and the normal matrix of the global program
function drawCylinder() {
    setMV() ;
    Cylinder.draw() ;
}

// Draws a cone along z of height 1 centered at the origin
// and base radius 1.0.
// Sets the modelview matrix and the normal matrix of the global program
function drawCone() {
    setMV() ;
    Cone.draw() ;
}

// Post multiples the modelview matrix with a translation matrix
// and replaces the modeling matrix with the result
function gTranslate(x,y,z) {
    modelMatrix = mult(modelMatrix,translate([x,y,z])) ;
}

// Post multiples the modelview matrix with a rotation matrix
// and replaces the modeling matrix with the result
function gRotate(theta,x,y,z) {
    modelMatrix = mult(modelMatrix,rotate(theta,[x,y,z])) ;
}

// Post multiples the modelview matrix with a scaling matrix
// and replaces the modeling matrix with the result
function gScale(sx,sy,sz) {
    modelMatrix = mult(modelMatrix,scale(sx,sy,sz)) ;
}

// Pops MS and stores the result as the current modelMatrix
function gPop() {
    modelMatrix = MS.pop() ;
}

// pushes the current modelViewMatrix in the stack MS
function gPush() {
    MS.push(modelMatrix) ;
}


/*  
    Where its called: In the render() function 
    Purpose: To draw the ground box on this the entirety of the scence is built
*/
function drawGroundBox(){
    setColor(vec4(-1,-1,-1,1))
    gTranslate(0,-35,0);
    gScale(20,30,20)
    drawCube();
}

/*  
    Where its called: In the render() function 
    Purpose: To draw the rocks in the scene, one small rock and one bigger rock from which three strands of seaweed are coming out
*/
function drawRocks(){
    setColor(vec4(0.5,0.5,0.5,1)) 
    gScale(0.75,0.75,0.75)
    gTranslate(8,-12.45,0) ;
    drawSphere() ;

    gScale(1.75,1.75,1.75)
    gTranslate(1.6,0.5,0) ;
    drawSphere() ;
}

/*  
    Where its called: In the render() function 
    Purpose: Draws the initial seaweed ellipses, helps in setting up for the fish revolution around seaweeds
*/
function firstSeaWeeds(){
    setColor(vec4(0,1,0,1.5))
    gScale(0.2,0.6,0.2)

    gTranslate(34,-13,0)
    drawSphere();

    gTranslate(13,0,0)
    drawSphere();

    gTranslate(-6.4,1.8,0)
    gRotate(-180/3.14159*TIME/2,0,1,0)
    drawSphere() ;
}

/*  
    Where its called: In the render() function 
    Purpose: To draw fish (body,head,eyes,tail) and make it move up and down in waveform manner, also to make the tail fin flap back and forth
*/
function fishMovement(){
    gRotate(-290/3.14159,0,1,0)
        //Body
        {
            setColor(vec4(1.0,0.0,0.0,1.0)) ;
            gScale(12,5.15,14)
            gTranslate(0,1,2)

            yBodyMove = 1*Math.cos(1*TIME+2)
            gTranslate(0,yBodyMove,0)

            gRotate(360/3.14159,0,1,0);
            gScale(0.25,0.3,1)

            drawCone() ;
        }

        //Head
        {
            setColor(vec4(1.0,1.0,0.0,1.0)) ;
            gRotate(270/3.14159,0,1,0);
            gRotate(290/3.14159,0,1,0);
            gScale(1,1,0.5)
            gTranslate(0,0,1.5)
            drawCone();
        }

        //Left Eye
        gPush();
        {
            setColor(vec4(1.0,1.0,1.0,1.0)) ;
            gScale(0.25,0.35,0.15)
            gTranslate(-1.7,1.3,-0.5)

            drawSphere();
        }

        {
            setColor(vec4(-1.0,-1.0,-1.0,1.0)) ;            
            gScale(0.5,0.5,0.5)
            gTranslate(-0.5,0.2,1.5)

            drawSphere();
        }
        gPop();

        //Right Eye
        gPush();
        {
            setColor(vec4(1.0,1.0,1.0,1.0)) ;
            gScale(0.25,0.35,0.15)
            gTranslate(1.7,1.3,-0.5)

            drawSphere();
        }

        {
            setColor(vec4(-1.0,-1.0,-1.0,1.0)) ;            
            gScale(0.5,0.5,0.5)
            gTranslate(0.5,0.2,1.5)

            drawSphere();
        }
        gPop();

        //Tail
        gPush();
        {
            gRotate(290/3.14159,0,1,0)
            gRotate(-270/3.14159,0,1,0)
            tailMove = 7*Math.cos(15*TIME)
            gRotate(tailMove,0,1,0)
            
            gPush();
            {
                setColor(vec4(1.0,0.0,1.0,1.0)) ;
                gTranslate(0,0.8,-2.5)
                gRotate(-350/3.14159,1,0,0)
                gScale(0.25,0.25,1.75)
                drawCone();
            }
            gPop(); 
            
            gPush();
            {
                setColor(vec4(1.0,0.0,1.0,1.0)) ;
                gTranslate(0,-0.5,-2.5)
                gRotate(350/3.14159,1,0,0)
                gScale(0.25,0.25,1.25)

                drawCone();
            }
            gPop();
        }
    gPop();
}

/*  
    Where its called: In the render() function 
    Purpose: To draw the remaining 9 ellipses for all seaweed strands and to model their movement
*/
function allSeaWeeds(){
    // gTranslate(0,1,0)
    // drawSphere();

    var i;
    var phase = 0;
    for (i=0; i<9; i++){
        gTranslate(0,1,0)
        gRotate(20*Math.cos(1*TIME+phase),0,0,1)  
        gTranslate(0,1,0)
        phase++;
        drawSphere();
    }
}

/*  
    Where its called: In the render() function 
    Purpose: To draw the diver(head,body,legs), make the whole diver move up and down in the x,y direction and make the legs flap
*/
function drawDiver(){
    {
        gTranslate(18,5,0) ;
        setColor(vec4(0.5,0.0,0.7,1.0)) ;
        gRotate(180/3.14159,0,1,0) ;
        gScale(0.75,2.5,1.5)
        
        yCube = 0.5*Math.cos(0.5*TIME)
        xCube = 0.5*Math.cos(0.5*TIME)
        gTranslate(xCube,yCube,0)
        drawCube() ;
    }

    //Head
    {
        gTranslate(0,1.3,0)
        gScale(0.6,0.3,0.5)
        drawSphere()
    }

    //Left Leg
    gPush();
    {
        {   
            gTranslate(0,-9,-1.25)
            gRotate(80/3.14159,0,0,1)
            gScale(0.45,2,0.45)
            legWiggle = 7*Math.cos(1*TIME+0)
            gRotate(legWiggle,0,0,1)
            drawCube();
        }

        gTranslate(2.5,-1.7,0)
        gRotate(220/3.14159,0,0,1)
        gScale(0.25,2,1)
        drawCube();

        gScale(1.5,0.2,1)
        gTranslate(-1,-4,0)
        drawCube()

    }
    gPop();

    //Right Leg
    gPush();
    {
        {   
            gTranslate(1,-9,0.9)
            gRotate(80/3.14159,0,0,1)
            gScale(0.45,2,0.45)
            legWiggle = -7*Math.cos(1*TIME+0)
            gRotate(legWiggle,0,0,1)
            drawCube();
        }

        gTranslate(2.5,-1.7,0)
        gRotate(220/3.14159,0,0,1)
        gScale(0.25,2,1)
        drawCube();

        gScale(1.5,0.2,1)
        gTranslate(-1,-4,0)
        drawCube()
    }
    gPop();
}


function render() {
    
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    eye = vec3(0,0,10);
    MS = [] ; // Initialize modeling matrix stack
	
	// initialize the modeling matrix to identity
    modelMatrix = mat4() ;
    
    // set the camera matrix
    viewMatrix = lookAt(eye, at , up);
   
    // set the projection matrix
    projectionMatrix = ortho(left, right, bottom, ytop, near, far);
    
    // Rotations from the sliders
    gRotate(RZ,0,0,1) ;
    gRotate(RY,0,1,0) ;
    gRotate(RX,1,0,0) ;
    
    
    // set all the matrices
    setAllMatrices() ;
    
    var curTime ;
    if( animFlag )
    {
        curTime = (new Date()).getTime() /1000 ;
        if( resetTimerFlag ) {
            prevTime = curTime ;
            resetTimerFlag = false ;
        }
        TIME = TIME + curTime - prevTime ;
        prevTime = curTime ;
    }
   
    //////////////////////////////////////////////////////////////////////
    ////          Beginning of where the functions are called          ///
    //////////////////////////////////////////////////////////////////////

    //Calling the drawGroundBox function
    gPush();
    {   
        drawGroundBox();
    }
    gPop();

    //Translating and scaling down the whole scence to a suitable position and size before rendering other objects
    gTranslate(-5,0,0) ;
    gScale(0.5,0.5,0.5)

    //Calling the drawRocks function 
    gPush();
    {
        drawRocks();
    }
    gPop();

    /*
        Calling the functions to draw the first ellipses for the seaweeds and to draw the fish (including its movement)
        Both these function calls are within a push() pop() because the fish revolution depends on the seaweeds rotation
    */
    gPush();
    {   
        firstSeaWeeds();
        fishMovement();
    }
    gPop();

    //Calling the drawDiver function
    gPush();
    {
        drawDiver();
    }
    gPop();

    /*
        Calling the function which makes the remaining 9 ellipses for the seaweeds and handles their movement 
    */
    setColor(vec4(0,1,0,1.5))
    gScale(0.2,0.6,0.2)
    gPush();
    {
        gPush();
        {
            gTranslate(34,-13,0)
            allSeaWeeds()
        }
        gPop();
    
        gPush();
        {
            gTranslate(40.6,-11.3,0)
            allSeaWeeds()
        }
        gPop();
    
        gPush();
        {
            gTranslate(47,-13,0)
            allSeaWeeds();
        }
        gPop();
    }
    gPop();
    ////////////////////////////////////////////////////////////////
    ////          End of where the functions are called          ///
    ////////////////////////////////////////////////////////////////

    if( animFlag )
        window.requestAnimFrame(render);
}

// A simple camera controller which uses an HTML element as the event
// source for constructing a view matrix. Assign an "onchange"
// function to the controller as follows to receive the updated X and
// Y angles for the camera:
//
//   var controller = new CameraController(canvas);
//   controller.onchange = function(xRot, yRot) { ... };
//
// The view matrix is computed elsewhere.
function CameraController(element) {
	var controller = this;
	this.onchange = null;
	this.xRot = 0;
	this.yRot = 0;
	this.scaleFactor = 3.0;
	this.dragging = false;
	this.curX = 0;
	this.curY = 0;
	
	// Assign a mouse down handler to the HTML element.
	element.onmousedown = function(ev) {
		controller.dragging = true;
		controller.curX = ev.clientX;
		controller.curY = ev.clientY;
	};
	
	// Assign a mouse up handler to the HTML element.
	element.onmouseup = function(ev) {
		controller.dragging = false;
	};
	
	// Assign a mouse move handler to the HTML element.
	element.onmousemove = function(ev) {
		if (controller.dragging) {
			// Determine how far we have moved since the last mouse move
			// event.
			var curX = ev.clientX;
			var curY = ev.clientY;
			var deltaX = (controller.curX - curX) / controller.scaleFactor;
			var deltaY = (controller.curY - curY) / controller.scaleFactor;
			controller.curX = curX;
			controller.curY = curY;
			// Update the X and Y rotation angles based on the mouse motion.
			controller.yRot = (controller.yRot + deltaX) % 360;
			controller.xRot = (controller.xRot + deltaY);
			// Clamp the X rotation to prevent the camera from going upside
			// down.
			if (controller.xRot < -90) {
				controller.xRot = -90;
			} else if (controller.xRot > 90) {
				controller.xRot = 90;
			}
			// Send the onchange event to any listener.
			if (controller.onchange != null) {
				controller.onchange(controller.xRot, controller.yRot);
			}
		}
	};
}
