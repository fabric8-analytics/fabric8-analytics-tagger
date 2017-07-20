FROM registry.centos.org/centos/centos:7
MAINTAINER Fridolin Pokorny <fridolin@redhat.com>

ENV LANG=en_US.UTF-8

RUN useradd coreapi

COPY ./ /tmp/kw_install/

# Download also NLTK's punkt for word_tokenize()
RUN yum install -y epel-release &&\
  yum install -y python34-devel python34-pip &&\
  yum clean all &&\
  pushd /tmp/kw_install &&\
  pip3 install . &&\
  popd &&\
  rm -rf /tmp/kw_install &&\
  python3 -c 'import nltk; nltk.download("punkt");'

COPY hack/run_tagger.sh /usr/bin/

USER coreapi
CMD ["/usr/bin/run_tagger.sh"]
