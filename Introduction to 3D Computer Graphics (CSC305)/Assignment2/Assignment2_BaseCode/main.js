/*

    Name: Vedant Manawat
    VNumber: V00904582

    March 17th 2021
    CSC 305 Assignment 2


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


// var lightPosition2 = vec4(100.0, 100.0, 100.0, 1.0 );
var lightPosition = vec4(100.0,0.0,100, 1.0 );

var lightAmbient = vec4(0.5, 0.5, 0.2, 1.0 );
var lightDiffuse = vec4( 1.0, 1.0, 1.0, 1.0 );
var lightSpecular = vec4( 1.0, 1.0, 1.0, 1.0 );

var materialAmbient = vec4( 1.0, 0.0, 1.0, 1.0 );
var materialDiffuse = vec4( 1.0, 0.8, 0.0, 1.0 );
var materialSpecular = vec4( 0.4, 0.4, 0.4, 1.0 );
var materialShininess = 100.0;


var ambientColor, diffuseColor, specularColor;

var modelMatrix, viewMatrix ;
var modelViewMatrix, projectionMatrix, normalMatrix;
var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc;
var eye;
var at = vec3(0.0, 0.0, 0.0);
var up = vec3(0.0, 1.0, 0.0);

var RX = 0 ;
var RY = 0 ;
var RZ = 0 ;

var MS = [] ; // The modeling matrix stack
var TIME = 0.0 ; // Realtime
var TIME = 0.0 ; // Realtime
var resetTimerFlag = true ;
var animFlag = false ;
var prevTime = 0.0 ;
var useTextures = 0 ;

var then = 0;
var timeToDisplay = 0;

// ------------ Images for textures stuff --------------
var texSize = 64;

var image1 = new Array()
for (var i =0; i<texSize; i++)  image1[i] = new Array();
for (var i =0; i<texSize; i++)
for ( var j = 0; j < texSize; j++)
image1[i][j] = new Float32Array(4);
for (var i =0; i<texSize; i++) for (var j=0; j<texSize; j++) {
    var c = (((i & 0x8) == 0) ^ ((j & 0x8)  == 0));
    image1[i][j] = [c, c, c, 1];
}

// Convert floats to ubytes for texture

var image2 = new Uint8Array(4*texSize*texSize);

for ( var i = 0; i < texSize; i++ )
for ( var j = 0; j < texSize; j++ )
for(var k =0; k<4; k++)
image2[4*texSize*i+4*j+k] = 255*image1[i][j][k];


var textureArray = [] ;

function isLoaded(im) {
    if (im.complete) {
        console.log("loaded") ;
        return true ;
    }
    else {
        console.log("still not loaded!!!!") ;
        return false ;
    }
}

function loadFileTexture(tex, filename)
{
    tex.textureWebGL  = gl.createTexture();
    tex.image = new Image();
    tex.image.src = filename ;
    tex.isTextureReady = false ;
    tex.image.onload = function() { handleTextureLoaded(tex); }
    // The image is going to be loaded asyncronously (lazy) which could be
    // after the program continues to the next functions. OUCH!
}

function loadImageTexture(tex, image) {
    tex.textureWebGL  = gl.createTexture();
    tex.image = new Image();
    //tex.image.src = "CheckerBoard-from-Memory" ;
    
    gl.bindTexture( gl.TEXTURE_2D, tex.textureWebGL );
    //gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0,
                  gl.RGBA, gl.UNSIGNED_BYTE, image);
    gl.generateMipmap( gl.TEXTURE_2D );
    gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER,
                     gl.NEAREST_MIPMAP_LINEAR );
    gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); //Prevents s-coordinate wrapping (repeating)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); //Prevents t-coordinate wrapping (repeating)
    gl.bindTexture(gl.TEXTURE_2D, null);

    tex.isTextureReady = true ;

}

function initTextures() {
    

    //Adding the texture for the water to the texture array (source for image is provided in the README)
    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"Textures/water.png") ;
    
    //Adding the texture for the boat to the texture array (source for image is provided in the README)
    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"Textures/wood.jpg") ;

    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"Textures/mountain.png") ;

    textureArray.push({}) ;
    loadFileTexture(textureArray[textureArray.length-1],"Textures/Sun.jpg") ;
    
}


function handleTextureLoaded(textureObj) {
    gl.bindTexture(gl.TEXTURE_2D, textureObj.textureWebGL);
	gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); // otherwise the image would be flipped upsdide down
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, textureObj.image);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); //Prevents s-coordinate wrapping (repeating)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); //Prevents t-coordinate wrapping (repeating)
    gl.bindTexture(gl.TEXTURE_2D, null);
    console.log(textureObj.image.src) ;
    
    textureObj.isTextureReady = true ;
}

//----------------------------------------------------------------

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

function toggleTextures() {
    useTextures = 1 - useTextures ;
    gl.uniform1i( gl.getUniformLocation(program,"useTextures"), useTextures );
}

function waitForTextures1(tex) {
    setTimeout( function() {
    console.log("Waiting for: "+ tex.image.src) ;
    wtime = (new Date()).getTime() ;
    if( !tex.isTextureReady )
    {
        console.log(wtime + " not ready yet") ;
        waitForTextures1(tex) ;
    }
    else
    {
        console.log("ready to render") ;
        window.requestAnimFrame(render);
    }
               },5) ;
    
}

// Takes an array of textures and calls render if the textures are created
function waitForTextures(texs) {
    setTimeout( function() {
               var n = 0 ;
               for ( var i = 0 ; i < texs.length ; i++ )
               {
                    console.log("boo"+texs[i].image.src) ;
                    n = n+texs[i].isTextureReady ;
               }
               wtime = (new Date()).getTime() ;
               if( n != texs.length )
               {
               console.log(wtime + " not ready yet") ;
               waitForTextures(texs) ;
               }
               else
               {
               console.log("ready to render") ;
               window.requestAnimFrame(render);
               }
               },5) ;
    
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
    
 
    // Load canonical objects and their attributes
    Cube.init(program);
    Cylinder.init(9,program);
    Cone.init(9,program) ;
    Sphere.init(36,program) ;

    gl.uniform1i( gl.getUniformLocation(program, "useTextures"), useTextures );

    // record the locations of the matrices that are used in the shaders
    modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix" );
    normalMatrixLoc = gl.getUniformLocation( program, "normalMatrix" );
    projectionMatrixLoc = gl.getUniformLocation( program, "projectionMatrix" );
    
    // set a default material
    setColor(materialDiffuse) ;
    
  
    
    // set the callbacks for the UI elements
    document.getElementById("sliderXi").oninput = function() {
        RX = this.value ;
        window.requestAnimFrame(render);
    };
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
    };
    
    document.getElementById("textureToggleButton").onclick = function() {
        toggleTextures() ;
        window.requestAnimFrame(render);
    };

    var controller = new CameraController(canvas);
    controller.onchange = function(xRot,yRot) {
        RX = xRot ;
        RY = yRot ;
        // window.requestAnimFrame(render);
    };
    
    // load and initialize the textures
    initTextures() ;
    
    // Recursive wait for the textures to load
    waitForTextures(textureArray) ;
    //setTimeout (render, 100) ;
    
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
// and replaces the modelview matrix with the result
function gTranslate(x,y,z) {
    modelMatrix = mult(modelMatrix,translate([x,y,z])) ;
}

// Post multiples the modelview matrix with a rotation matrix
// and replaces the modelview matrix with the result
function gRotate(theta,x,y,z) {
    modelMatrix = mult(modelMatrix,rotate(theta,[x,y,z])) ;
}

// Post multiples the modelview matrix with a scaling matrix
// and replaces the modelview matrix with the result
function gScale(sx,sy,sz) {
    modelMatrix = mult(modelMatrix,scale(sx,sy,sz)) ;
}

// Pops MS and stores the result as the current modelMatrix
function gPop() {
    modelMatrix = MS.pop() ;
}

// pushes the current modelMatrix in the stack MS
function gPush() {
    MS.push(modelMatrix) ;
}

// Function to draw the cubes that will represent the ocean
// This function will handle the drawing of the cubes as well as the movements in x and y direction 
// to replicatet the motion of waves
function drawOcean(){
    var wave1 = 0.2*Math.cos(0.5*TIME + 0.2);
    var back_and_forth = 0.2*Math.cos(0.5*TIME);

    setColor(vec4(0,0.5,1,-1));
    gTranslate(-6,-6.5,0);
    gScale(2,-2,9);
    gTranslate(-back_and_forth,wave1,0);
    drawCube();

    var wave2 = -0.2*Math.cos(0.3*TIME + 0.1);
    gTranslate(2,-0.15,0);
    gTranslate(0,wave2,0);
    drawCube();

    var wave3 = 0.2*Math.cos(0.2*TIME + 0.1);
    gTranslate(2,0.15,0);
    gTranslate(0,wave3,0);
    drawCube();

    var wave4 = -0.2*Math.cos(0.1*TIME + 0.1);
    gTranslate(2,-0.15,0);
    gTranslate(0,wave4,0);
    drawCube();
}

// Function to draw the boat that the fisherman will be sitting on
// This function handles the drawing of the cube as well as its oscillation in the y direction 
function drawBoat(){

    // Boat body
    setColor(vec4(0.79,0.64,0.44,1));
    gScale(1.5,0.3,0.1);
    gTranslate(-3,-3,0);
    var boat_move = -0.2*Math.cos(1*TIME + 0.1);
    gTranslate(0,boat_move,0);
    drawCube();

    gPush();
    {   
        gRotate(-280/3.14159,1,0,0);
        gScale(0.75,0.75,1)
        gTranslate(1.5,0,-0.65)
        gRotate(280/3.14159,0,1,0);
        gRotate(90/3.14159,0,1,0);
        gScale(1,2,2)
        drawCone();
    }
    gPop();

    gPush();
    {   
        gRotate(-280/3.14159,1,0,0);
        gScale(0.75,0.75,1)
        gTranslate(-1.5,0,-0.65)
        gRotate(-280/3.14159,0,1,0);
        gRotate(-90/3.14159,0,1,0);
        gScale(1,2,2)
        drawCone();
    }
    gPop();

    toggleTextures();
    gPush();
    {
        setColor(vec4(0,0,0,1));
        gTranslate(0,-1.1,0);
        gScale(0.85,0,0.85);
        drawCube();
    }
    gPop();
    toggleTextures();
}

// Function to draw the fisherman 
// What is being drawn here:
//  - Fisherman Body 
//  - Fisherman Head 
//  - Hat (on the head)
//  - Fishermans two arms
// This function is also responsible to make the fishermans forearms move up and down in the y direction, 
// consequently, the fishing rod will also be moving up and down in the y direction. 
function drawFisherMan(){

    // Draw Body 
    setColor(vec4(0.5,0,1,1));
    gScale(0.2,1.6,0.5)
    gTranslate(1.8,-1.5,0);
    drawCube();

    // Draw Head
    setColor(vec4(1,0.85,0.72,1));
    gScale(0.8,0.5,1);
    gTranslate(0,-3,0);
    drawSphere();

    //Draw Hat
    gPush();
    {   
        setColor(vec4(0.75,0.75,0.25,1));
        gRotate(280/3.14159,1,0,0);
        gScale(2,2,1);
        gTranslate(0,0,1);
        drawCone();
    }
    gPop();


    // Draw Both Arms
    gPush();
    {   
        //Near arm/hand
        gPush();
        {   
            setColor(vec4(0,0,1,1));
            gRotate(-40/3.14159,0,1,0);
            gRotate(-100/3.14159,0,0,1);
            gScale(0.45,1,0.3);
            gTranslate(-1.5,3,3);
            drawCube();
        }
        gPop();

        gPush();
        {   
            setColor(vec4(1,0.85,0.72,1));
            gRotate(70/3.14159,0,1,0);
            gRotate(180/3.14159,0,0,1);
            gScale(0.45,1.2,0.3);
            gTranslate(7.2,0,5);

            var move = 5*Math.cos(5*TIME);
            gRotate(-move,0,0,1);
            drawCube();
        }
        gPop();
    }
    gPop();
    
    //Far arm/hand
    gPush();
    {
        gPush();
        {   
            setColor(vec4(0,0,1,1));
            gRotate(40/3.14159,0,1,0);
            gRotate(-100/3.14159,0,0,1);
            gScale(0.45,1,0.3);
            gTranslate(-1,3,-3.5);
            drawCube();
        }
        gPop();

        gPush();
        {   
            setColor(vec4(1,0.85,0.72,1));
            gRotate(-70/3.14159,0,1,0);
            gRotate(180/3.14159,0,0,1);
            gScale(0.45,1.2,0.3);
            gTranslate(7.2,0,-5.5);

            var move = 5*Math.cos(5*TIME);
            gRotate(-move,0,0,1);
            drawCube();

            
            // Draw Fishing Rod
            setColor(vec4(0,0,0,1));
            gRotate(200/3.14159,0,1,0);
            gRotate(180/3.14159,0,0,1);
            gRotate(-90/3.14159,0,1,1);
            gScale(0.3,4,0.3);
            gTranslate(-2.5,-1,4);
            drawCube();
        }
        gPop();
    }
    gPop();
}


// Function to draw the clouds
function drawCloud(){
    setColor(vec4(0.82,0.82,0.82,1));
    gScale(0.35,0.35,0.35);
    drawSphere();

    gPush();
    {
        gTranslate(1,0,0);
        drawSphere();

        gPush();
        {
            gTranslate(0,1.3,0);
            drawSphere();

            gPush();
            {
                gTranslate(1,1,0);
                drawSphere();
            }
            gPop();

            gTranslate(1,0,0);
            drawSphere();

            gPush();
            {
                gTranslate(0,0,1);
                drawSphere();

                gTranslate(0,0,-2);
                drawSphere();
            }
            gPop();

            gTranslate(1,0,0);
            drawSphere();
        }
        gPop();

        gTranslate(0,0,-1);
        drawSphere();

        gTranslate(0,0,2);
        drawSphere();
    }
    gPop();

    gPush();
    {
        gTranslate(2,0,0);
        drawSphere();

        gTranslate(0,0,-1);
        drawSphere();

        gTranslate(0,0,2);
        drawSphere();
    }
    gPop();

    gPush();
    {
        gTranslate(3,0,0);
        drawSphere();

        gTranslate(0,0,-1);
        drawSphere();

        gTranslate(0,0,2);
        drawSphere();
    }
    gPop();

    gTranslate(4,0,0);
    drawSphere();
}


// This function is responsible to set up the background of the scene 
// What is being drawn here:
// - Two mountains 
// - One Sun
// - Clouds (this function calls the drawClouds() function after setting the locations of where to darw them). 
// This function also handles the movement of the clouds.
function drawBackground(){
    // Moiuntains
    toggleTextures();
    gPush();
    {
        setColor(vec4(0.82,0.41,0.11,1))
        gRotate(-280/3.14159,1,0,0);

        gScale(6,4,7);
        gTranslate(-0.5,3,-0.3);
        drawCone();

        gScale(1,1,2);
        gTranslate(1,0,0);
        drawCone();
    }
    gPop();
    toggleTextures();

    // Clouds
    gPush();
    {   
        // Cloud 1 + its movement
        gPush();
        {   
            gTranslate(-5.5,1.5,-7);
            gTranslate(0.05*TIME,0,0);
            
            drawCloud();
        }
        gPop();

        // Cloud 2 + its movement
        gPush();
        {
            gTranslate(-1.5,1.5,-19);
            gTranslate(0.04*TIME,0,0);
            
            drawCloud();
        }
        gPop();

        // Cloud 3 + its movement
        gPush();
        {
            gTranslate(2.5,1.5,-7);
            gTranslate(0.02*TIME,0,0);
            
            drawCloud();
        }
        gPop();
    }
    gPop();    
}

function drawSun(){
    gPush();
    {   
        setColor(vec4(0.98,0.83,0.25));
        gScale(0.75,0.75,0.75);
        gTranslate(-5,6,-15);
        drawSphere();
    }
    gPop();
}

function render() {
    
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    //Changing the background color to a sunset orange 
    gl.clearColor(0.99, 0.36, 0.32, 0.75);

    // Updating the position of the eye
    eye = vec3(0,16,50);

    // Using parametric equations of a circle to implement the 360 fly around for the camera. 
    eye[0] = -50*Math.sin(0.15*TIME);   
    eye[2] = 50*Math.cos(0.15*TIME);

    // set the projection matrix
    projectionMatrix = ortho(left, right, bottom, ytop, near, far);
    
    // set the camera matrix
    viewMatrix = lookAt(eye, at , up);
    
    // initialize the modeling matrix stack
    MS= [] ;
    modelMatrix = mat4() ;
    
    // apply the slider rotations
    gRotate(RZ,0,0,1) ;
    gRotate(RY,0,1,0) ;
    gRotate(RX,1,0,0) ;
    
    // send all the matrices to the shaders
    setAllMatrices() ;
    
    // get real time
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
    
    // ********** LOADING IN THE TEXTURES ********** //
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, textureArray[0].textureWebGL);
    gl.uniform1i(gl.getUniformLocation(program, "texture1"), 0);
    
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, textureArray[1].textureWebGL);
    gl.uniform1i(gl.getUniformLocation(program, "texture2"), 1);

    gl.activeTexture(gl.TEXTURE2);
    gl.bindTexture(gl.TEXTURE_2D, textureArray[2].textureWebGL);
    gl.uniform1i(gl.getUniformLocation(program, "texture3"), 2);

    gl.activeTexture(gl.TEXTURE3);
    gl.bindTexture(gl.TEXTURE_2D, textureArray[3].textureWebGL);
    gl.uniform1i(gl.getUniformLocation(program, "texture4"), 3);

    // ******************************************** //

    var isSea = 1;
    var isBoat = 0; 
    var isMountain = 0;
    var isSun = 0;

    // BEGINNING OF WHERE THE FUNCTIONS ARE CALLED TO DRAW THE SCENE
    gScale(0.75,0.75,0.75);
    gPush();
    {   
        toggleTextures();
        // Setting the ocean texture
        var currTIME = TIME
        gl.bindTexture(gl.TEXTURE_2D, textureArray[0].textureWebGL);
        gl.uniform1i( gl.getUniformLocation(program,"isSea"), isSea );
        gl.uniform1i( gl.getUniformLocation(program,"isBoat"), isBoat ); 
        gl.uniform1f( gl.getUniformLocation(program,"currTIME"), currTIME ); 
        // Function call to draw the ocean
        drawOcean();
        toggleTextures();

        toggleTextures();
        // Setting the boat texture
        isSea = 0;
        isBoat = 1;
        gl.bindTexture(gl.TEXTURE_2D, textureArray[1].textureWebGL);
        gl.uniform1i( gl.getUniformLocation(program,"isSea"), isSea );
        gl.uniform1i( gl.getUniformLocation(program,"isBoat"), isBoat ); 
        // Function call to darw the boat
        drawBoat();    
        toggleTextures();

        // Function to draw the fisherman
        drawFisherMan();

    }
    gPop();

    gPush();
    {   
        // Function to draw the background (Mountains, Sun and Clouds)
        isSea = 0;
        isBoat = 0;
        isMountain = 1;
        gl.bindTexture(gl.TEXTURE_2D, textureArray[2].textureWebGL);
        gl.uniform1i( gl.getUniformLocation(program,"isSea"), isSea );
        gl.uniform1i( gl.getUniformLocation(program,"isBoat"), isBoat ); 
        gl.uniform1i( gl.getUniformLocation(program,"isMountain"), isMountain ); 
        drawBackground();


        toggleTextures();
        isSea = 0;
        isBoat = 0;
        isMountain = 0;
        isSun = 1;
        gl.bindTexture(gl.TEXTURE_2D, textureArray[3].textureWebGL);
        gl.uniform1i( gl.getUniformLocation(program,"isSea"), isSea );
        gl.uniform1i( gl.getUniformLocation(program,"isBoat"), isBoat ); 
        gl.uniform1i( gl.getUniformLocation(program,"isMountain"), isMountain ); 
        gl.uniform1i( gl.getUniformLocation(program,"isSun"), isSun ); 
        drawSun();
        toggleTextures();

    }
    gPop();

    // ***** Calculating FPS ***** /

    if(animFlag){
        const fpsElem = document.querySelector("#fps");
        var temp;
        var now = TIME;
        const timeElapsed = now - then;
        temp = now - timeToDisplay
        const fps = Math.floor(1/timeElapsed);
        then = now;

        if (temp > 2){
            timeToDisplay = now;
            fpsElem.textContent = fps.toFixed(1);
        }
        window.requestAnimFrame(render);
    }
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
