## update backend modules ##
cp /home/bennyray/Projects/neuro-learn/web/neurolearn_dev/backend/views.py /home/bennyray/Projects/neuro-learn/docker/dev/app/backend/

## update frontend static ##
# rm -rf /home/bennyray/Projects/neuro-learn/docker/dev/app/frontend/dist/
# cp -r /home/bennyray/Projects/neuro-learn/web/neurolearn_dev/frontend/dist/ /home/bennyray/Projects/neuro-learn/docker/dev/app/frontend/
# source /home/bennyray/Projects/neuro-learn/web/neurolearn_dev/env/bin/activate
# cd /home/bennyray/Projects/neuro-learn/docker/dev/app/
# python manage.py collectstatic