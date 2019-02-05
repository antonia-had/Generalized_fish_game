NSAMPLES=4000
METHOD=Latin
JAVA_ARGS="-cp ./MOEAFramework-2.12-Demo.jar"

# Generate the parameter samples
echo -n "Generating parameter samples..."
java ${JAVA_ARGS} \
    org.moeaframework.analysis.sensitivity.SampleGenerator \
    --method ${METHOD} --n ${NSAMPLES} --p parameters.txt \
    --o parameter_samples.txt
