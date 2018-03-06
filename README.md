--- 
date: 06 March 2018
author: Alberto Costa
affiliation: Future Cities Laboratory, Singapore
version: 0.1
---

# EDMF
This package contains 3 files:
* edmf.py: main source file including the functions to perform error-domain model falsification
* Template_Input.xlsx: input file with data. 
* test.py: a file to show how to use the code

## Input file details
The file must contain the following sheets:
* Pred: the first row represent the labels of the columns, and must be there. First there are the parameters names, then the sensor names. The number of parameters must be provided when calling the constructor (see test.py file). Each subsequent row contains data.
* Pred_Err: the first row contains labels. From the second row there are data. In the first two columns (c1 and c2) there are two numerical values. In the third column the allowed values are "r", "a", "g". "r" means that the uncertainty is relative, so c1 and c2 are the relative lower and upper bound of the uniform distribution (it means that their values will be multiplied by the corresponding mean computed from data). If "a", the uncertainty is absolute, so the values c1 and c2 are already the lower and upper bounds of the uniform distribution. If "g", the uncertainty is gaussian. c1 is the mean and c2 is the standard deviation. After that, there is a value of 0/1 for each subsequent cell (c4, c5...), one for each sensor, to indicate if the corresponding uncertainty is affecting (1) or not (0) the sensor (e.g., if c4=1 it means that sensor 1 is affected by the uncertainty defined by c1,c2,c3 of that row). 
* Meas: one column. The first row is the label (e.g., Measurements), then there are the measurement values.
*Meas_Err: same as for Pred_Err, but related to the uncertainties affecting the measurements.





This package has been tested with Python 2.7 on Mac running OS X.



THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT
HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.